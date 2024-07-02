# GUI and main functions of the program
# Calls the backend functions through button presses from relevant files
# FF Tobias

import analyse, feedback, readfiles
# import gui <-- funktioniert noch nicht
import streamlit as st
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

analyse.analysetext
feedback.generatefeedback
readfiles.readfiles

if 'stage' not in st.session_state:
    st.session_state.stage = 0

root.wm_attributes('-topmost', 1)

def set_state(i):
    st.session_state.stage = i