# GUI and main functions of the program
# Calls the backend functions through button presses from relevant files
# FF Tobias

import analyse, feedback, readfiles
import streamlit as st
import pandas as pd
import tkinter as tk
from tkinter import filedialog

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

inputlist = ["File", "Folder"]
with st.sidebar:
    st.title('Choose input')
    

with col1:
    inputtype = st.selectbox("Choose input type", inputlist)
    if(st.button("Select thesis")):
        if inputtype == "File":
            # Reading in single thesis file goes here
            pass
        elif inputtype == "Folder":
            # Reading in folder of thesis files goes here
            pass
with col2:
    st.button("col2 button")
with col3:
    st.button("col3 button")