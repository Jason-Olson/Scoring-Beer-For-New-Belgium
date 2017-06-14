import pandas as pd
import numpy as np
import pickle
import spacy
from result_for_brew_num import score_batch,preprocess



if __name__ == '__main__':
    df = pd.read_pickle('data/df_pickle.pickle')
    dfu = pd.DataFrame(df['BrewNumber'].unique())
    # samp = dfu.sample(60)
    samp = dfu
    out_list = []
    if not 'nlp' in locals():
        print("Loading English Module...")
        nlp = spacy.load('en')
    for i,x in enumerate(samp.values):
        print(i)
        dfbn = df[df['BrewNumber'] == x[0]]
        dfbn = preprocess(dfbn,nlp)
        out_dict = score_batch(dfbn)
        out_list.append(out_dict)
    out_list = np.array(out_list)
    samp['results_dict'] =  out_list
    writer = pd.ExcelWriter('data/sample_output2.xlsx')
    samp.to_excel(writer,'sample_results')
    writer.save()
