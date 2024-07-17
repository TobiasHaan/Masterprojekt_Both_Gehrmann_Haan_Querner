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

st.set_page_config(layout='wide')
root = tk.Tk()
root.withdraw()
root.wm_attributes('-topmost', 1)
headers = ['Title', 'Page count', 'Word count', 'Avg. word length', 'Sentence count', 'Avg. sentence length', 'Figure count']

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

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


# def calcavg(dataframe):
#     for row in dataframe.rows: # iterate over every row, add all of them and divide through amount
#         value = value + dataframe[row]

#     return averages

col11, col12 = st.columns(2)
col1, col2, col3 = st.columns(3)

with st.sidebar: # Sidebar is accessible regardless of state
    st.title('Thesis Analyser')
    if(st.button('Load CSV')):
        mycsv = loadcsv()
        st.write(mycsv)
    if(st.button('Save to CSV')):
        saver = loadcsv()
        saver.to_csv('./data/thesis.csv')
    uploaded_files = st.file_uploader('Load thesis files for database', type="pdf", accept_multiple_files=True)
    thesis_uploader = st.file_uploader('Load own thesis for analysis', type="pdf", accept_multiple_files=True)


    if(uploaded_files): # To save in CSV
        for uploaded_file in uploaded_files:
            input_pdf = uploaded_file.name
            with open(input_pdf, "wb") as f:
                f.write(uploaded_file.getbuffer())
            text = extract_text(input_pdf)
            num_sentences = len(sent_tokenize(text, language='german'))
            total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
            avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0
            tocsv = []
            tocsv = [input_pdf,'0',total_words,'0',num_sentences,avg_sentence_length,'0'] #Title, Page count, Word count, Avg. word length, Sentence count, Avg. sentence length, Figure count
            df = pd.DataFrame(tocsv, headers)
            df2 = loadcsv()
            df2.insert(column=len(df2.columns)+1, loc=len(df.columns)+1, value=df)
            df2.to_csv('./data/thesis.csv')

    if(thesis_uploader): # For analysis
        for thesis in thesis_uploader:
            input_pdf = thesis.name
            with open(input_pdf, "wb") as f:
                f.write(thesis.getbuffer())
            text = extract_text(input_pdf)
            num_sentences = len(sent_tokenize(text, language='german'))
            total_words = sum(len(word_tokenize(sentence, language='german')) for sentence in sent_tokenize(text, language='german'))
            avg_sentence_length = total_words / num_sentences if num_sentences > 0 else 0
            comparer = loadcsv()


            #st.write(comparer)
            comparer = comparer.transpose()
            comparer = comparer.drop(columns="Title")
            comparer["Page count"] = pd.to_numeric(comparer["Page count"])
            comparer["Word count"] = pd.to_numeric(comparer["Word count"])
            comparer["Avg. word length"] = pd.to_numeric(comparer["Avg. word length"])
            comparer["Sentence count"] = pd.to_numeric(comparer["Sentence count"])
            comparer["Avg. sentence length"] = pd.to_numeric(comparer["Avg. sentence length"])
            comparer["Figure count"] = pd.to_numeric(comparer["Figure count"])
            st.write(comparer)
            averages = comparer.mean()
            averages = pd.DataFrame(averages)
            averages = averages.rename_axis('Values').rename_axis('attributes', axis='columns')
            myaverages = {"Page count": [0], "Word count" : [total_words], "Avg. word length" : [0], "Sentence count": [num_sentences], "Avg. sentence length": [avg_sentence_length], "Figure count": [0]}
            myaverages = pd.Series(myaverages)
            averages.insert(column=len(averages.columns), loc=len(averages.columns), value=myaverages)
            averages.columns
            #st.write(averages.columns.names())
            st.write(averages.columns)
            st.table(averages)
            

if st.session_state.stage == 0: # State for data selection and analysis preparation
    st.expander("")

    with col1:
        st.title("Figure types")
        check_box = st.checkbox("Box plots")
        if(check_box):
            storage.createbox = True
        else:
            storage.createbox = False
        check_vio = st.checkbox("Violin plots")
        if(check_vio):
            gui.switchviolin()
        check_sca = st.checkbox("Scatter plots")
        if(check_sca):
            gui.switchscatter()
        st.write(storage.createbox,storage.createviolin, storage.createscatter)
    with col2:
        st.title("Data points to analyse")
        check_pcn = st.checkbox("Page count")
        if(check_pcn):
            gui.switchpcn()
        check_wcn = st.checkbox("Word count")
        if(check_wcn):
            gui.switchwcn()
        check_wln = st.checkbox("Average word length") 
        if(check_wln):
            gui.switchwln()
        check_scn = st.checkbox("Sentence count")
        if(check_scn):
            gui.switchscn()
        check_sln = st.checkbox("Average sentence length")
        if(check_sln):
            gui.switchsln()
        check_fcn = st.checkbox("Figure count")
        if(check_fcn):
            gui.switchfcn()

if(st.button("Create graphs")):
    if(check_box or check_vio or check_sca):
        try:
            gui.grapher("box", storage.data)
            set_state(1)
        except AttributeError and TypeError:
            col3.write("Ensure data is loaded beforehand!")


if st.session_state.stage == 1: # State for results

    with col11:
        st.title("Data overview")

        graphs = st.expander('Figures')
        with graphs:
            if(storage.createbox):
                st.write("I should create box plots now!")
                #grapher("box", storage.data)
            else:
                st.write("Load data first!")
            if(storage.createviolin):
                st.write("I should create violin plots now!")
                #grapher("box", storage.data)
            else:
                st.write("Load data first!")
            if(storage.createscatter):
                st.write("I should create scatter plots now!")
                #grapher("box", storage.data)
            else:
                st.write("Load data first!")


    with col12:
        st.title("Thesis feedback")
    
