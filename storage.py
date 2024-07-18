import pandas as pd

global data
data = pd.DataFrame
global createbox, createviolin, createscatter, pgn, wcn, wln, scn, sln, fcn
createbox, createviolin, createscatter, pcn, wcn, wln, scn, sln, fcn = (False,)*9
global averages
averages = pd.DataFrame