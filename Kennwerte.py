import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')
import spacy
nlp = spacy.load('de_core_web_sm')
import pathlib
import collections
from statistics import mean



def kennwerte(txt):
    '''Kennwerte für die Textanalyse berechnen. 
    Bisher grundlegende Ausgaben definiert: Wortanzahl, durchschnittliche Wortlänge, Satzanzahl, durchschnittliche Satzlänge,
    Anzahl Absätze, durchschnittliche Wortzahl pro Absatz, % Nomen, % Verben.'''
    words = nltk.word_tokenize(txt, 'german')
    worte = len(words)
    wortlen = mean([len(w) for w in words])
    sent = nltk.sent_tokenize(txt, 'german')
    satze = len(sent)
    satzlen = worte/satze
    absatze = len(txt.split('\n'))
    wabsatz = worte/absatze

    # Spacy erst einmal mit Nomen und Verben
    res = [token.pos_ for token in txt]
    nomen = collections.Counter(res)['NOUN']
    nomenperc = nomen/worte
    verben = collections.Counter(res)['VERB']
    verbenperc = verben/worte
    adj = collections.Counter(res)['ADJ']
    adjperc = adj/worte
    return worte, wortlen, satze, satzlen, absatze, wabsatz, nomenperc, verbenperc, adjperc



# Mock-Text einlesen
file_name = 'BA.txt'
#with open('BA.txt', 'r') as t:
#    txt = t.read()
# Spacy-Variante mit pathlib
txt = nlp(pathlib.Path(file_name).read_text(encoding='utf-8'))

# Ausgabe als Text, später für Datengrundlage und Ausgabe zu verwerten
w1, w2, s1, s2, a1, a2, np, vp, ap = kennwerte(txt)
print('Wortanzahl: ' + str(w1) + '\ndurchschnittliche Wortlänge: ' + str(w2) + '\nSatzanzahl: ' + str(s1) + '\ndurchschnittliche Satzlänge: ' + str(s2) + '\nAbsatzanzahl: ' + str(a1) + '\ndurchschnittliche Wortzahl pro Absatz: ' + str(a2) + '\nNomen %: ' + str(np) + '\nVerben %: ' + str(vp) + '\nAdjektive &: ' + str(ap))