import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')
from statistics import mean



def kennwerte(txt):
    '''Kennwerte für die Textanalyse berechnen. 
    Bisher grundlegende Ausgaben definiert: Wortanzahl, durchschnittliche Wortlänge, Satzanzahl, durchschnittliche Satzlänge.'''
    words = nltk.word_tokenize(txt, 'german')
    worte = len(words)
    wortlen = mean([len(w) for w in words])
    sent = nltk.sent_tokenize(txt, 'german')
    satze = len(sent)
    satzlen = worte/satze
    return worte, wortlen, satze, satzlen



# Mock-Text einlesen
file_path = 'BA.txt'
with open('BA.txt', 'r') as t:
    txt = t.read()

# Ausgabe als Text, später für Datengrundlage und Ausgabe zu verwerten
w1, w2, s1, s2 = kennwerte(txt)
print('Wortanzahl: ' + str(w1) + '\ndurchschnittliche Wortlänge: ' + str(w2) + '\nSatzanzahl: ' + str(s1) + '\ndurchschnittliche Satzlänge: ' + str(s2))