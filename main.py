# GUI and main functions of the program
# Calls the backend functions through button presses from relevant files
# FF Tobias

import analyse, feedback, readfiles, storage, gui
import streamlit as st
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pymupdf
import nltk
import fitz
from nltk.tokenize import sent_tokenize, word_tokenize
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import re
from statistics import mean
import PyPDF2

st.set_page_config(layout='wide')
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)
headers = ['Title', 'Page count', 'Word count', 'Avg. word length', 'Sentence count', 'Avg. sentence length', 'Figure count']

state = st.session_state


if 'stage' not in state:
    state.stage = 0

def set_state(i):
    state.stage = i

#@st.cache_data
def loadcsv():
    df = pd.read_csv('./data/thesis.csv', sep=',', header = None, index_col = 0, skiprows=1)
    storage.data = df
    return df

def extract_text(file):
    doc = pymupdf.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text      

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

def analyze_consistency(explanations):
    explanation_counts = defaultdict(int)
    for explanation in explanations:
        explanation_counts[explanation] += 1

    inconsistent_explanations = {exp: count for exp, count in explanation_counts.items() if count == 1}
    
    # Debugging print statements
    print(f"Explanation Counts: {dict(explanation_counts)}")
    print(f"Inconsistent Explanations: {inconsistent_explanations}")

    return inconsistent_explanations

def annotate_pdf_with_feedback(input_pdf, output_pdf, feedback):
    doc = fitz.open(input_pdf)
    inconsistency_pages = set()  # Use a set to track unique pages with inconsistencies
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        for explanation in feedback:
            if explanation in text:
                highlight_area = page.search_for(explanation)
                if highlight_area:
                    inconsistency_pages.add(page_num + 1)  # Add page number to set (1-indexed)
                    for rect in highlight_area:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_colors(stroke=(1, 0, 0))  # Red highlight
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

def add_chart_to_pdf(input_pdf, chart_image, output_pdf):
    doc = fitz.open(input_pdf)
    doc.new_page()  # Add a new page at the end of the PDF document
    
    # Get the last page (newly added page)
    page = doc[-1]
    
    # Insert the chart image
    rect = fitz.Rect(0, 0, 595, 842)  # A4 size in points (72 points per inch)
    page.insert_image(rect, filename=chart_image)
    
    # Use incremental save when modifying an existing PDF
    doc.save(output_pdf, incremental=True, encryption=doc.is_encrypted)

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

col1, col2 = st.columns(2)
#create_graphs = st.button("Create graphs")
col11, col12 = st.columns(2)

with st.sidebar: # Sidebar is accessible regardless of state
    st.title('Thesis Analyser')
    if(st.button('Reset')):
        set_state(0)
    if(st.button('Load CSV')):
        try:
            mycsv = loadcsv()
            st.write("Loading successful")
            st.write("Loaded CSV with ", len(storage.data.columns), "thesis files.")
        except FileNotFoundError:
            st.write("File not found, ensure the thesis.csv file is located in ./data/")
    if(st.button('Save to CSV')):
        if not storage.data.empty:
            saver = storage.data
            saver.to_csv('./data/thesis.csv')
            st.write("Saving successful")
            st.write("Wrote ", len(saver.columns), " thesis files into CSV")
        else:
            st.write("Nothing to save.")
    uploaded_files = st.file_uploader('Load thesis files for database', type="pdf", accept_multiple_files=True)
    thesis_uploader = st.file_uploader('Load own thesis for analysis', type="pdf", accept_multiple_files=True)


    if(uploaded_files): # To save in CSV
        for uploaded_file in uploaded_files:
            input_pdf = uploaded_file.name
            with open(input_pdf, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text = extract_text(input_pdf)
            
            reader = PyPDF2.PdfFileReader(input_pdf)
            num_pages = reader.getNumPages()
            num_sentences = len(sent_tokenize(text, language='german'))
            total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
            words = nltk.word_tokenize(text, 'german')
            worte = len(words)
            wortlen = mean([len(w) for w in words])
            avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0

            tocsv = []
            tocsv = [input_pdf,num_pages,total_words,wortlen,num_sentences,avg_sentence_length,'0'] #Title, Page count, Word count, Avg. word length, Sentence count, Avg. sentence length, Figure count
            df = pd.DataFrame(tocsv, headers)
            df2 = loadcsv()
            storage.data.insert(column=len(storage.data.columns)+1, loc=len(df.columns)+1, value=df)
            #print(storage.data)
            #storage.data = df2
            #df2.to_csv('./data/thesis.csv')

    if(thesis_uploader): # For analysis
        col12.title("Thesis Feedback")
        for thesis in thesis_uploader:
            input_pdf = thesis.name
            with open(input_pdf, "wb") as f:
                f.write(thesis.getbuffer())
            text = extract_text(input_pdf)
            results = 0

            reader = PyPDF2.PdfFileReader(input_pdf)
            num_pages = reader.getNumPages()
            explanations = identify_definitions_explanations(text)
            inconsistent_explanations = analyze_consistency(explanations)
            output_pdf = f"annotated_{input_pdf}"
            inconsistency_pages = annotate_pdf_with_feedback(input_pdf, output_pdf, inconsistent_explanations)
            pages_with_inconsistencies = ', '.join(map(str, sorted(inconsistency_pages))) if inconsistency_pages else 'None'
            count_of_inconsistencies = len(inconsistency_pages)



            num_sentences = len(sent_tokenize(text, language='german'))
            total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
            words = nltk.word_tokenize(text, 'german')
            worte = len(words)
            wortlen = mean([len(w) for w in words])
            avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0

            data = []
            data.append({
            'Titel Dokument': input_pdf,
            'Anzahl der Sätze': num_sentences,
            'Durchschnittliche Satzlänge': avg_sentence_length,
            'Anzahl der Inkonsistenzen': count_of_inconsistencies,
            'Seiten mit Inkonsistenzen': pages_with_inconsistencies
            })

            chart_image = f"chart_{input_pdf}.png"
            generate_comparative_chart(data, input_pdf, chart_image)
            add_chart_to_pdf(output_pdf, chart_image, output_pdf)

            with open(output_pdf, "rb") as file:
                col12.download_button(
                    label=f"Download annotated {input_pdf}",
                    data=file,
                    file_name=output_pdf,
                    mime="application/pdf"
                )




            comparer = loadcsv()


            #st.write(comparer)
            comparer = comparer.transpose()
            #comparer = comparer.drop(columns="Title")
            comparer["Page count"] = pd.to_numeric(comparer["Page count"])
            comparer["Word count"] = pd.to_numeric(comparer["Word count"])
            comparer["Avg. word length"] = pd.to_numeric(comparer["Avg. word length"])
            comparer["Sentence count"] = pd.to_numeric(comparer["Sentence count"])
            comparer["Avg. sentence length"] = pd.to_numeric(comparer["Avg. sentence length"])
            comparer["Figure count"] = pd.to_numeric(comparer["Figure count"])
            #st.write(comparer)
            averages = comparer.mean()
            averages = pd.DataFrame(averages)
            averages = averages.rename_axis('Values').rename_axis('attributes', axis='columns')
            myaverages = {"Page count": num_pages, "Word count" : total_words, "Avg. word length" : wortlen, "Sentence count": num_sentences, "Avg. sentence length": avg_sentence_length, "Figure count": results}
            myaverages = pd.Series(myaverages)
            #storage.averages = myaverages
            averages.insert(column=len(averages.columns), loc=len(averages.columns), value=myaverages)

            col12.table(averages)
            


#if state.stage == 0: # State for data selection and analysis preparation
    #st.write(state.stage)

with col1:
    ftypes = st.title("Figure types")
    check_box = st.checkbox("Box plots")
    if(check_box):
        storage.createbox = True
    else:
        storage.createbox = False
    check_vio = st.checkbox("Violin plots")
    if(check_vio):
        storage.createviolin = True
    else:
        storage.createviolin = False
    #check_sca = st.checkbox("Scatter plots")
    # if(check_sca):
    #     storage.createscatter = True
    # else:
    #     storage.createscatter = False  
with col2:
    st.title("Data points to analyse")
    check_pcn = st.checkbox("Page count")
    if(check_pcn):
        storage.pcn = True
    else:
        storage.pcn = False
    check_wcn = st.checkbox("Word count")
    if(check_wcn):
        storage.wcn = True
    else:
        storage.wcn = False
    check_wln = st.checkbox("Average word length") 
    if(check_wln):
        storage.wln = True
    else:
        storage.wln = False
    check_scn = st.checkbox("Sentence count")
    if(check_scn):
        storage.scn = True
    else:
        storage.scn = False
    check_sln = st.checkbox("Average sentence length")
    if(check_sln):
        storage.sln = True
    else:
        storage.sln = False
    check_fcn = st.checkbox("Figure count")
    if(check_fcn):
        storage.fcn = True
    else:
        storage.fcn = False

with col11:
    st.title("Data overview")

    if(storage.createbox):
        with st.expander('Boxplots'):
        #st.write("I should create box plots now!")
            try:
                gui.pcngrapher("box", storage.data)
                gui.wcngrapher("box", storage.data)
                gui.wlngrapher("box", storage.data)
                gui.scngrapher("box", storage.data)
                gui.slngrapher("box", storage.data)
                gui.fcngrapher("box", storage.data)
            except TypeError:
                st.write("Load data first!")

    if(storage.createviolin):
        with st.expander('Violinplots'):
        #st.write("I should create violin plots now!")
            try:
                gui.pcngrapher("violin", storage.data)
                gui.wcngrapher("violin", storage.data)
                gui.wlngrapher("violin", storage.data)
                gui.scngrapher("violin", storage.data)
                gui.slngrapher("violin", storage.data)
                gui.fcngrapher("violin", storage.data)
            except TypeError:
                st.write("Load data first!")
    if(storage.createscatter):
        #st.write("I should create scatter plots now!")
        gui.grapher("scatter", storage.data)
    else:
        st.write("Choose at least one plot type.")


with col12:
    pass
    #st.title("Thesis feedback")
    
