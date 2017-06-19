import sqlite3
import datetime
# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.resources import INLINE
from histogram_ttb_score import make_histo
from violin_ttb import make_violin
from ttb_score_stats import get_summary,remove_outliers,get_cut_threshold
from word_cloud import word_cloud_by_df
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
        nlp.vocab["thin"].is_stop = False

df = pd.read_pickle('data/df_pickle.pickle')
dfs = pd.read_pickle('data/full_run.pickle')

out_dict = get_summary(dfs)
ttb_out = remove_outliers(out_dict)
thres = get_cut_threshold(ttb_out)


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
    i = np.random.randint(10,200)
    print(i)
    text = request.form['text']
    # text = 160112004
    name_string = "  |  ".join(df.loc[(df['BrewNumber']==float(text)) & (df['isValidated']==1),'RegName'].values)
    results = dfs.loc[dfs[0]==float(text),'results_dict'].values[0]
    # out_results = []
    # for res in results:
    #     if res[1] >= .01:
    #         out_results.append(res)
    # processed_text = text.upper()
    # return processed_text

    print('here')
    out_violin = 'static/images/ttb_violin{}.png'.format(int(i))
    print(out_violin)
    out_hist = 'static/images/histogram_ttb{}.png'.format(int(i))
    out_word = 'static/images/word_cloud{}.png'.format(int(i))


    point = 0
    for row in results:
        if row[0] == "TTB":
            point = row[1]
    make_violin(ttb_out,thres,out_violin,point)

    df_s_curr = dfs.loc[dfs[0]==float(text)]
    make_histo(df_s_curr,out_hist)


    df_com_cur = df.loc[(df['BrewNumber']==float(text)) & (df['isValidated']==1)]
    word_cloud_by_df(df_com_cur,nlp,out_word)

    i += 1
    return render_template(
        'index.html',
        b_num = text,
        results_tup = results,
        name = name_string,
        out_v = out_violin,
        out_h = out_hist,
        out_w = out_word)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8105, debug=True)
