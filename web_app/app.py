import sqlite3
import datetime
# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.resources import INLINE
from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np
import requests
import json
import spacy

if not 'nlp' in locals():
        print("Loading English Module...")
        nlp = spacy.load('en')

df = pd.read_pickle('data/df_pickle.pickle')
dfs = pd.read_pickle('data/full_run.pickle')

app = Flask(__name__)

# We'd normally include configuration settings in this call

@app.route('/')
def index():

    is_fraud = "Hi"
    prio = '4'
    name = 'me'
    return render_template(
        'index.html',
        fraud = is_fraud,
        priority = prio,
        name = name)

#170111001.0
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    name_string = "  |  ".join(df.loc[(df['BrewNumber']==float(text)) & (df['isValidated']==1),'RegName'].values)
    results = dfs.loc[dfs[0]==float(text),'results_dict'].values[0]
    out_results = []
    for res in results:
        if res[1] >= .01:
            out_results.append(res)
    # processed_text = text.upper()
    # return processed_text
    return render_template(
        'index.html',
        b_num = text,
        results_tup = out_results,
        name = name_string)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8105, debug=True)
