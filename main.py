# GUI and main functions of the program
# Calls the backend functions through button presses from relevant files
# FF Tobias

import analyse, feedback, readfiles
import streamlit as st
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pymupdf

import nltk
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
import numpy as np

root = tk.Tk()
root.withdraw()

#analyse.analysetext
#feedback.generatefeedback
#readfiles.readfiles

if 'stage' not in st.session_state:
    st.session_state.stage = 0

st.set_page_config(layout='wide')

st.title("Thesis Analyser")
col1, col2, col3 = st.columns(3)

root.wm_attributes('-topmost', 1)

def set_state(i):
    st.session_state.stage = i

with st.sidebar:
    st.title('Choose input')
    

headers = ['Title', 'Page count', 'Word count', 'Avg. word length', 'Sentence count', 'Avg. sentence length', 'Figure count']
testdata = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing']

with col1:
    if(st.button("Read CSV")):
        mycsv = pd.read_csv('./data/thesis.csv', sep=',', header = None)
        
    if(st.button("Write CSV")):
        np.savetxt('./data/thesis.csv', [p for p in zip(headers, testdata)], delimiter=',', fmt='%s')
    #st.write(mycsv)
    #st.write(headers, testdata)
with col2:
    st.button("col2 button")
    
with col3:
    st.button("col3 button")