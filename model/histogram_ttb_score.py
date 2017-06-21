import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.close('all')


def make_histo(df,outfile):
    score_tup_list = df.iloc[0,1]
    x_labels = [x[0] for x in score_tup_list]
    y_values = [x[1] for x in score_tup_list]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 3))
    x_axis = np.arange(len(x_labels))
    width = .6
    y_corr = y_values
    y_poss = np.ones_like(y_corr)
    ax.bar(x_axis,y_poss,width,color='#F7DC6F')
    ax.bar(x_axis,y_corr,width,color='#d62728')
    ax.set_xticks(x_axis)
    ax.set_xticklabels(x_labels,fontsize=8,rotation=315,ha='left')
    ax.set_ylim(0., 1)
    ax.set_ylabel('Percentile (%)', fontsize=8)
    fig.patch.set_facecolor('#ffffe6')
    ax.set_title('TTB Score Summary', fontsize=14)
    plt.tight_layout()
    plt.savefig(outfile,dpi=400,facecolor=fig.get_facecolor(), edgecolor='none')
    return x_labels, y_values



if __name__ == '__main__':
    dffr = pd.read_pickle('data/full_run.pickle')
    df = dffr.sample(1,random_state=22)
    x_labels, y_values = make_histo(df,'graphs/histogram_ttb_r.png')
