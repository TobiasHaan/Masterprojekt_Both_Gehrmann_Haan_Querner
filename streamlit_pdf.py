import streamlit as st
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ensure the punkt data is downloaded
nltk.download('punkt')

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text, doc.page_count

# Function to analyze text
def analyze_text(text):
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    total_length = sum(len(sentence.split()) for sentence in sentences)
    average_sentence_length = total_length / num_sentences if num_sentences > 0 else 0
    return num_sentences, average_sentence_length

# Function to process multiple PDFs
def process_pdfs(files):
    results = []
    for file in files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        text, num_pages = extract_text_from_pdf(file.name)
        num_sentences, avg_sentence_length = analyze_text(text)
        results.append({
            "Dateiname": file.name,
            "Seitenanzahl": num_pages,
            "Anzahl Sätze": num_sentences,
            "Durchschn. Satzlänge (Wörter)": avg_sentence_length
        })
    return results

# Streamlit app setup
st.title("Auswertung Abschlussarbeiten")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = process_pdfs(uploaded_files)

    # Convert the results to a DataFrame
    df_results = pd.DataFrame(results)

    # Display the results in a table
    st.write("## Ergebnisse")
    st.table(df_results)

    # Calculate average values
    avg_pages = df_results["Seitenanzahl"].mean()
    avg_sentences = df_results["Anzahl Sätze"].mean()
    avg_sentence_length = df_results["Durchschn. Satzlänge (Wörter)"].mean()

    st.write(f"**Average Seitenanzahl:** {avg_pages:.2f}")
    st.write(f"**Average Anzahl Sätze:** {avg_sentences:.2f}")
    st.write(f"**Average Sentence Length:** {avg_sentence_length:.2f} words")

    # Create a bar chart
    st.write("## Diagramm")

    fig, ax = plt.subplots()
    x_labels = df_results["Dateiname"]
    page_counts = df_results["Seitenanzahl"]
    sentence_counts = df_results["Anzahl Sätze"]
    sentence_lengths = df_results["Durchschn. Satzlänge (Wörter)"]

    bar_width = 0.2
    index = np.arange(len(df_results))

    bar1 = ax.bar(index, page_counts, bar_width, label='Seiten')
    bar2 = ax.bar(index + bar_width, sentence_counts, bar_width, label='Sätze')
    bar3 = ax.bar(index + 2 * bar_width, sentence_lengths, bar_width, label='Satzlänge')

    ax.set_xlabel('PDF-Dokumente')
    ax.set_ylabel('Werte')
    ax.set_title('PDF Auswertung')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(x_labels, rotation=45, ha="right")
    ax.legend()

    st.pyplot(fig)
