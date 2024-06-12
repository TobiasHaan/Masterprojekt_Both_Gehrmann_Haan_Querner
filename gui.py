import streamlit as st
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

data = {'Words': [1217, 3121, 2214, 1859, 2938],
        'Images': [14, 2, 9, 0, 11],
        'Paragraphs': [9, 12, 48, 12, 1]
}

df = pd.DataFrame(data)

if 'stage' not in st.session_state:
    st.session_state.stage = 0

root.wm_attributes('-topmost', 1)

def set_state(i):
    st.session_state.stage = i
 

st.sidebar.button('Reset', on_click=set_state, args=[0])
st.sidebar.button('Load files', on_click=set_state, args=[1])
st.sidebar.button('Create specification file', on_click=set_state, args=[2])
st.sidebar.button('Analyse thesis', on_click=set_state, args=[3])
#st.sidebar.button('Analysis', on_click=set_state, args=[4])


if st.session_state.stage == 0: #Start State
    st.write("Welcome to the thesis tester. As of now, many of the featuers are not implemented yet, and this version is supposed to showcase the rough graphical user interface (GUI) for future users.")

if st.session_state.stage == 1: #Load Spec State


    if(st.button('Choose folder')):
        dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
    
    if(st.button('Choose file')):
        filename = st.text_input('Selected file:', filedialog.askopenfilenames(master=root))
        if(st.button('Load files to system')):
            st.write("Loaded files will be analyzed and used to create a dataframe containing countable data such as word count, number of images used, paragraphs etc.")
    
   

if st.session_state.stage == 2: #Create Spec State
    if(st.button("Analyse Dataframe")):
        st.bar_chart(data=df.Words, use_container_width=True)   
        st.bar_chart(data=df.Images, use_container_width=True)
        st.bar_chart(data=df.Paragraphs, use_container_width=True)
    if(st.button("Calculate averages")):
        st.write("Average number of words used:",df.loc[:, 'Words'].mean())
        st.write("Average number of images used:",df.loc[:, 'Images'].mean())
        st.write("Average number of paragraphs used:",df.loc[:, 'Paragraphs'].mean())
    if(st.button("Create file")):
        st.text_input(label="File name")


if st.session_state.stage == 3: #Thesis analysis state
    if(st.button("Load thesis")):
        filename = st.text_input('Selected thesis:', filedialog.askopenfilename(master=root))
    if(st.button("Analyse")):
        st.write("No thesis loaded.")

#if st.session_state.stage == 4: #Analysis
#    if(st.button("Analysis")):
#        st.write("Test")
