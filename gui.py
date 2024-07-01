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

thdata = {'Words': [1217],
        'Images': [14],
        'Paragraphs': [9]
}

avgdata = {'Words': [],
        'Images': [],
        'Paragraphs': []}

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
    
    if(st.button('Choose files')):
        filename = st.text_input('Selected files:', filedialog.askopenfilenames(master=root))
    if(st.button('Load files to system')):
        st.write("Loaded files will be analyzed and used to create a dataframe containing countable data such as word count, number of images used, paragraphs etc.")
    
   

if st.session_state.stage == 2: #Create Spec State
    if(st.button("Analyse Dataframe")):
        st.write("Words per thesis")
        st.bar_chart(data=df.Words, use_container_width=True)
        st.write("Images per thesis")   
        st.bar_chart(data=df.Images, use_container_width=True)
        st.write("Paragraphs per thesis")
        st.bar_chart(data=df.Paragraphs, use_container_width=True)
    if(st.button("Calculate averages")):
        avgwords = df.loc[:, 'Words'].mean()
        avgimages = df.loc[:, 'Images'].mean()
        avgparagraphs = df.loc[:, 'Paragraphs'].mean()
        st.write("Average number of words used:",avgwords)
        st.write("Average number of images used:",avgimages)
        st.write("Average number of paragraphs used:",avgparagraphs)
        avgdata = {'Words': [avgwords],
        'Images': [avgimages],
        'Paragraphs': [avgparagraphs]}

    if(st.button("Create file")):
        st.text_input(label="File name")


if st.session_state.stage == 3: #Thesis analysis state
    if(st.button("Load thesis")):
        filename = st.text_input('Selected thesis:', filedialog.askopenfilename(master=root))
    if(st.button("Analyse")):
        #st.write("No thesis loaded.")
        st.write("Your thesis data")
        st.table(thdata)
        st.write("Average thesis data in comparison")
    dataw = {"Word count":[2269, 1217]}
    datai ={"Images":[7, 9]}
    datap ={"Paragraphs":[14, 16]}
    df1 = pd.DataFrame(dataw)
    df2 = pd.DataFrame(datai)
    df3 = pd.DataFrame(datap)
    #df
    st.bar_chart(df1)
    st.bar_chart(df2)
    st.bar_chart(df3)

#if st.session_state.stage == 4: #Analysis
#    if(st.button("Analysis")):
#        st.write("Test")
