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

# def calcavg(dataframe):
#     for row in dataframe.rows: # iterate over every row, add all of them and divide through amount
#         value = value + dataframe[row]

#     return averages


col1, col2, col3 = st.columns(3)
#create_graphs = st.button("Create graphs")
col11, col12 = st.columns(2)

with st.sidebar: # Sidebar is accessible regardless of state
    st.title('Thesis Analyser')
    if(st.button('Reset')):
        set_state(0)
    if(st.button('Load CSV')):
        mycsv = loadcsv()
        st.write("Loading successful")
    if(st.button('Save to CSV')):
        saver = loadcsv()
        saver.to_csv('./data/thesis.csv')
        st.write("Saving successful")
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
            storage.averages.insert(column=len(averages.columns), loc=len(averages.columns), value=myaverages)
            storage.averages.columns
            #st.write(averages.columns.names())
            st.write(averages.columns)
            st.table(averages)
            


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
    check_sca = st.checkbox("Scatter plots")
    if(check_sca):
        storage.createscatter = True
    else:
        storage.createscatter = False  
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

# with col3:
#     if(create_graphs):
#         if(check_box or check_vio or check_sca):
#             try:
#                 #gui.grapher("box", storage.data)
#                 set_state(1)
#                 #st.button("Visualize")
#             except AttributeError and TypeError:
#                 col3.write("Ensure data is loaded beforehand!")

#if state.stage == 1: # State for results
    #st.write(state.stage)
with col11:
    st.title("Data overview")

    #graphs = st.expander('Figures')
    #blots = st.expander('Boxplots')
    #with graphs:
    if(storage.createbox):
       with st.expander('Boxplots'):
        #st.write("I should create box plots now!")
            gui.pcngrapher("box", storage.data)
            gui.wcngrapher("box", storage.data)
            gui.wlngrapher("box", storage.data)
            gui.scngrapher("box", storage.data)
            gui.slngrapher("box", storage.data)
            gui.fcngrapher("box", storage.data)

    if(storage.createviolin):
        with st.expander('Violinplots'):
        #st.write("I should create violin plots now!")
            gui.pcngrapher("violin", storage.data)
            gui.wcngrapher("violin", storage.data)
            gui.wlngrapher("violin", storage.data)
            gui.scngrapher("violin", storage.data)
            gui.slngrapher("violin", storage.data)
            gui.fcngrapher("violin", storage.data)
    elif(storage.createscatter):
        #st.write("I should create scatter plots now!")
        gui.grapher("scatter", storage.data)
    else:
        st.write("Choose at least one plot type.")


with col12:
    st.title("Thesis feedback")
    
