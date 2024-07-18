# Tobias

import storage
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def pcngrapher(gtype,data):
    fig, ax = plt.subplots()  
    numpages = data.iloc[1].to_list()       # pcn -> Page count
    if storage.pcn:
        if gtype == "box":
            ax.set_ylabel('Number of pages')
            converter = list(map(float, numpages))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Number of pages')
            converter = list(map(float, numpages))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)
        # elif gtype == "scatter":
        #     ax.set_ylabel('Number of pages')
        #     converter = list(map(float, numpages))
        #     bplot = ax.violinplot(converter)
        #     st.pyplot(fig)

def wcngrapher(gtype,data):
    fig, ax = plt.subplots()  
    numwords = data.iloc[2].to_list()       # wcn -> Word count
    if storage.wcn:
        if gtype == "box":
            ax.set_ylabel('Number of words')
            converter = list(map(float, numwords))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Number of words')
            converter = list(map(float, numwords))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)

def wlngrapher(gtype,data):
    fig, ax = plt.subplots()  
    avgwordln = data.iloc[3].to_list()       # wln -> Word length
    if storage.wln:
        if gtype == "box":
            ax.set_ylabel('Word length')
            converter = list(map(float, avgwordln))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Word length')
            converter = list(map(float, avgwordln))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)

def scngrapher(gtype,data):
    fig, ax = plt.subplots()  
    numsen = data.iloc[4].to_list()       # scn -> Sentence count
    if storage.scn:
        if gtype == "box":
            ax.set_ylabel('Number of sentences')
            converter = list(map(float, numsen))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Number of sentences')
            converter = list(map(float, numsen))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)

def slngrapher(gtype,data):
    fig, ax = plt.subplots()  
    avgsenln = data.iloc[5].to_list()        # sln -> Sentence length
    if storage.sln:
        if gtype == "box":
            ax.set_ylabel('Sentence length')
            converter = list(map(float, avgsenln))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Sentence length')
            converter = list(map(float, avgsenln))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)

def fcngrapher(gtype,data):
    fig, ax = plt.subplots()  
    numfigs = data.iloc[6].to_list()       # fcn -> Figure count
    if storage.fcn:
        if gtype == "box":
            ax.set_ylabel('Number of figures')
            converter = list(map(float, numfigs))
            bplotpcn = ax.boxplot(converter)
            st.pyplot(plt.gcf(), clear_figure=True)
        elif gtype == "violin":
            ax.set_ylabel('Number of figures')
            converter = list(map(float, numfigs))
            bplot = ax.violinplot(converter)
            st.pyplot(fig)

def grapher(gtype, data):
    fig, ax = plt.subplots()    
    numpages = data.iloc[1].to_list()       # pcn -> Page count
    numwords = data.iloc[2].to_list()       # wcn -> Word count
    avgwordln = data.iloc[3].to_list()      # wln -> Word length
    numsen = data.iloc[4].to_list()         # scn -> Sentence count
    avgsenln = data.iloc[5].to_list()       # sln -> Sentence length
    numfigs = data.iloc[6].to_list()        # fcn -> Figure count
    num_of_thesis = data.count              #      
    #converter = list(map(int, converter))
    #numpages = list(map(int, numpages))
    if gtype == "box":
        # if storage.pcn:
        #     ax.set_ylabel('Number of pages')
        #     converter = list(map(float, numpages))
        #     bplotpcn = ax.boxplot(converter)
        #     st.pyplot(plt.gcf())
        #     st.pyplot(clear_figure=True)
        if storage.wcn:
            ax.set_ylabel('Number of words')
            converter = list(map(float, numwords))
            bplotwcn = ax.boxplot(converter)
            st.pyplot(fig)
        if storage.wln:
            ax.set_ylabel('Word length')
            converter = list(map(float, avgwordln))
            bplot = ax.boxplot(converter)
            st.pyplot(fig)
        if storage.scn:
            ax.set_ylabel('Number of sentences')
            converter = list(map(float, numsen))
            bplot = ax.boxplot(converter)
            st.pyplot(fig)
        if storage.sln:
            ax.set_ylabel('Sentence length')
            converter = list(map(float, avgsenln))
            bplot = ax.boxplot(converter)
            st.pyplot(fig)
        if storage.fcn:
            ax.set_ylabel('Number of figures')
            converter = list(map(float, numfigs))
            bplot = ax.boxplot(converter)
            st.pyplot(fig)            
    elif gtype == "violin":
        bplot = ax.violinplot(converter)
        st.pyplot(fig)
    elif gtype == "scatter":
        bplot = ax.scatter(converter,converter)
        #bplot = ax.scatter(converter)
        st.pyplot(fig)        
    #st.pyplot(plt.gcf())
    
    #bplot2 = ax.violinplot(converter)
    #boxplot = mycsv.boxplot(column=['Col1', 'Col2', 'Col3']) 
    #st.pyplot(plt.gcf())
    #st.pyplot(bplot)