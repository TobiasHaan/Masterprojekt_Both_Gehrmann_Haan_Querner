import streamlit as st
import fitz  # PyMuPDF
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from collections import defaultdict

# Ensure the punkt tokenizer is downloaded
nltk.download('punkt')

# Load spaCy German model
nlp = spacy.load('de_core_news_sm')

# Function to extract text from a PDF
def extract_text(file):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()

    return text

# Function to identify definitions and explanations
def identify_definitions_explanations(text):
    definition_patterns = [
        r'\bdefiniert als\b',
        r'\bim Folgenden als\b',
        r'\bwird als\b',
    ]

    explanations = []
    sentences = sent_tokenize(text, language='german')
    for sentence in sentences:
        for pattern in definition_patterns:
            if re.search(pattern, sentence):
                explanations.append(sentence)
                break

    return explanations

# Function to analyze consistency
def analyze_consistency(explanations):
    explanation_counts = defaultdict(int)
    for explanation in explanations:
        explanation_counts[explanation] += 1

    inconsistent_explanations = {exp: count for exp, count in explanation_counts.items() if count == 1}
    
    # Debugging print statements
    print(f"Explanation Counts: {dict(explanation_counts)}")
    print(f"Inconsistent Explanations: {inconsistent_explanations}")

    return inconsistent_explanations

# Function to annotate PDF with feedback and return the page numbers
def annotate_pdf_with_feedback(input_pdf, output_pdf, feedback):
    doc = fitz.open(input_pdf)
    inconsistency_pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        for explanation in feedback:
            if explanation in text:
                highlight_area = page.search_for(explanation)
                if highlight_area:
                    inconsistency_pages.append(page_num + 1)  # Add 1 to make page numbers 1-indexed
                    for rect in highlight_area:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_colors(stroke=(1, 0, 0))  # Red color for highlights
                        highlight.update()

                    # Add a side comment
                    comment_rect = fitz.Rect(rect.x1 + 10, rect.y1, rect.x1 + 300, rect.y1 + 30)
                    comment = f"Inconsistent explanation: '{explanation}'"
                    page.add_freetext_annot(
                        comment_rect,
                        comment,
                        fontsize=10,
                        fontname="helv",
                        text_color=(1, 0, 0),
                        fill_color=(1, 1, 1),
                        border_color=(0, 0, 0)
                    )

    doc.save(output_pdf)
    return inconsistency_pages

# Function to generate comparative chart
def generate_comparative_chart(data, current_file, output_image):
    df = pd.DataFrame(data)
    
    current_file_data = df[df['Titel Dokument'] == current_file]
    other_files_data = df[df['Titel Dokument'] != current_file]
    avg_sentence_length_others = other_files_data['Durchschnittliche Satzlänge'].mean()

    plt.figure(figsize=(10, 5))
    plt.bar(current_file_data['Titel Dokument'], current_file_data['Durchschnittliche Satzlänge'], color='blue', label='Current File')
    plt.axhline(y=avg_sentence_length_others, color='r', linestyle='--', label='Durchschnitt der anderen')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Durchschnittliche Satzlänge')
    plt.legend()
    plt.title('Vergleichende Analyse der durchschnittlichen Satzlängen')
    
    plt.savefig(output_image)
    plt.close()

# Function to add chart to PDF
def add_chart_to_pdf(input_pdf, chart_image, output_pdf):
    doc = fitz.open(input_pdf)
    doc.new_page()  # Add a new page at the end of the document
    
    # Get the last page (newly added page)
    page = doc[-1]
    
    # Insert the chart image
    rect = fitz.Rect(0, 0, 595, 842)  # A4 size in points (72 points per inch)
    page.insert_image(rect, filename=chart_image)
    
    # Use incremental save when modifying an existing PDF
    doc.save(output_pdf, incremental=True, encryption=doc.is_encrypted)

# Function to format numbers to European style
def format_number(value, decimals=2):
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Streamlit app
st.title("Auswertung PDFs)")

uploaded_files = st.file_uploader("PDFs hochladen", type="pdf", accept_multiple_files=True)

if uploaded_files:
    data = []
    display_data = []  # For formatted display data
    for uploaded_file in uploaded_files:
        input_pdf = uploaded_file.name
        with open(input_pdf, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text
        text = extract_text(input_pdf)

        # Identify definitions and explanations
        explanations = identify_definitions_explanations(text)

        # Analyze consistency
        inconsistent_explanations = analyze_consistency(explanations)

        # Annotate PDF with feedback and get pages with inconsistencies
        output_pdf = f"annotated_{input_pdf}"
        inconsistency_pages = annotate_pdf_with_feedback(input_pdf, output_pdf, inconsistent_explanations)

        num_sentences = len(sent_tokenize(text, language='german'))
        total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
        avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0

        # Convert list of pages to a string
        pages_with_inconsistencies = ', '.join(map(str, inconsistency_pages)) if inconsistency_pages else 'None'

        # Adjust the count of inconsistencies by subtracting 1
        count_of_inconsistencies = max(0, len(inconsistent_explanations) - 1)

        data.append({
            'Titel Dokument': input_pdf,
            'Anzahl der Sätze': num_sentences,
            'Durchschnittliche Satzlänge': avg_sentence_length,
            'Anzahl der Inkonsistenzen': count_of_inconsistencies,
            'Seiten mit Inkonsistenzen': pages_with_inconsistencies
        })

        display_data.append({
            'Titel Dokument': input_pdf,
            'Anzahl der Sätze': format_number(num_sentences, 0),
            'Durchschnittliche Satzlänge': format_number(avg_sentence_length, 2),
            'Anzahl der Inkonsistenzen': count_of_inconsistencies,
            'Seiten mit Inkonsistenzen': pages_with_inconsistencies
        })

        # Generate and add comparative chart
        chart_image = f"chart_{input_pdf}.png"
        generate_comparative_chart(data, input_pdf, chart_image)
        add_chart_to_pdf(output_pdf, chart_image, output_pdf)

        # Provide download button for the annotated PDF
        with open(output_pdf, "rb") as file:
            st.download_button(
                label=f"Download annotated {input_pdf}",
                data=file,
                file_name=output_pdf,
                mime="application/pdf"
            )

    # Display the analysis results in a table
    df_display = pd.DataFrame(display_data)
    st.table(df_display)

    # Display a chart for average sentence lengths
    st.write("Durchschnittliche Satzlänge")
    plt.figure(figsize=(10, 5))
    plt.bar(df_display['Titel Dokument'], df_display['Durchschnittliche Satzlänge'].apply(lambda x: float(x.replace(',', '.'))), color=['blue', 'orange', 'green'])
    plt.axhline(y=pd.DataFrame(data)['Durchschnittliche Satzlänge'].mean(), color='r', linestyle='--', label='Durchschnitt')
    plt.xlabel('Titel Dokument')
    plt.ylabel('Durchschnittliche Satzlänge')
    plt.legend()
    st.pyplot(plt)
