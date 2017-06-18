import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from ttb_score_stats import get_data,get_summary,remove_outliers,get_cut_threshold

plt.style.use('ggplot')
plt.close('all')


def make_violin(ttb_out,thres,point = .90):
    thres = thres/100.0
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 2))

    axes.violinplot(ttb_out, points=200, vert=False, widths=1.1,
                          showmeans=True, showextrema=False, showmedians=False, bw_method=0.5)
    axes.axvline(x=thres)
    if point > thres:
        arrow_text = "TTB"
        red_background_start = .7
    else:
        arrow_text = "Not TTB"
        red_background_start = point -.025
    axes.axvspan(red_background_start, thres, facecolor='r', alpha=0.1)
    axes.axvspan(thres, 1, facecolor='g', alpha=0.1)
    axes.get_yaxis().set_ticks([1])
    axes.set_title('TTB Indicator', fontsize=14)
    axes.set_ylabel('Liklihood', fontsize=8)
    axes.set_xlabel('TTB Score', fontsize=8)
    axes.set_xlim([red_background_start, 1])
    axes.text(ttb_out.mean()-.005, 1.05, u'mean',rotation='vertical',fontsize=6,color="#F8766D")

    axes.plot([point], [1], 'o')
    axes.annotate(arrow_text, xy=(point, 1), xytext=(point+.01, 1.4),
                arrowprops=dict(facecolor='black', shrink=0.05))
    # axes.tick_params(axis='y',which='both',left='off',right='off')
    axes.set_yticklabels([])
    plt.tight_layout()
    fig.patch.set_facecolor('#ffffe6')
    plt.savefig('graphs/ttb_violin.png',dpi=400,facecolor=fig.get_facecolor(), edgecolor='none')

if __name__ == '__main__':
    df = get_data()
    out_dict = get_summary(df)
    ttb_out = remove_outliers(out_dict)
    thres = get_cut_threshold(ttb_out)
    make_violin(ttb_out,thres)
