# GUI and main functions of the program
# Calls the backend functions through button presses from relevant files
# FF Tobias

import analyse, feedback, readfiles, storage
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
headers = ['Title', 'Page count', 'Word count', 'Avg. word length', 'Sentence count', 'Avg. sentence length', 'Figure count']

#@st.cache_data
def loadcsv():
    df = pd.read_csv('./data/thesis.csv', sep=',', header = None, index_col = 0, skiprows=1)
    storage.data = df
    return df

def grapher(gtype, data):
    fig, ax = plt.subplots()
    ax.set_ylabel('average number')
    converter = data.iloc[1].to_list()
    converter = list(map(int, converter))
    bplot = ax.boxplot(converter)
    #st.pyplot(plt.gcf())
    st.pyplot(fig)
    #bplot2 = ax.violinplot(converter)
    #boxplot = mycsv.boxplot(column=['Col1', 'Col2', 'Col3']) 
    #st.pyplot(plt.gcf())
    #st.pyplot(bplot)

if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

st.set_page_config(layout='wide')
root.wm_attributes('-topmost', 1)

col1, col2 = st.columns(2)





with st.sidebar:
    st.title('Thesis Analyser')
    if(st.button('Load CSV')):
        mycsv = loadcsv()
        col1.write(mycsv)
        
    if(st.button('Save to CSV')):
        saver = loadcsv()
        col1.write(saver)
        saver.to_csv('./data/thesis.csv') 
    if(st.button('Load thesis files')):
        pass
    if(st.button('Load own thesis for analysis')):
        pass


with col1:
    st.title("Data overview")
    if(st.button("Create graphs")):
        try:
            grapher("box", storage.data)
        except AttributeError:
            col1.write("Ensure data is loaded beforehand!")
        

with col2:
    st.title("Thesis feedback")
