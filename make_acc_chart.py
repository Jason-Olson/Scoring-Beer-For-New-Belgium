import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

plt.style.use('ggplot')
plt.close('all')

def get_data():
    df = pd.read_pickle('data/flavor_acc.pickle')
    df = df.drop('wrong_dict',axis=1)
    names = df.pop('name').values
    col_names = list(df.columns)
    X =  df.values
    return X,col_names,names

def create_chart(X, col_names, names,outFile,y_top_lim):
    fig, axes = plt.subplots(ncols=1, nrows=int(len(col_names)/2),figsize=(10,10))#,figsize=(200,100)
    # fig, axes = plt.subplots(ncols=1, nrows=(X.shape[1]/2))
    # fig = plt.figure(figsize=(40,20))
    # ax = fig.add_subplot(111)
    x_axis = np.arange(len(names))
    width = .6
    for i,ax in enumerate(axes):
        xi = i*2
        y_corr = X[:,xi]
        y_poss = X[:,xi+1]
        ax.bar(x_axis,y_poss,width,color='#F7DC6F')
        ax.bar(x_axis,y_corr,width,color='#d62728')
        stop = min(col_names[xi].find('_'),12)
        ax.set_ylabel(col_names[xi][:stop],fontsize=4)
        ax.set_ylim(0., y_top_lim)
        ax.tick_params(axis='y',which='both',left='off',right='off')
        ax.get_yaxis().set_ticks([])
        if i ==int(len(col_names)/2-1):
            ax.set_xticks(x_axis)
            ax.set_xticklabels(names,rotation='vertical',fontsize=4)
        else:
            ax.tick_params(
                            axis='x',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom='off',      # ticks along the bottom edge are off
                            top='off',         # ticks along the top edge are off
                            labelbottom='off')

    # plt.tight_layout(pad=.1,w_pad=.01,h_pad=.1)
    fig.subplots_adjust(bottom=.075,top=.975,left=.025,right=.975)
    plt.subplots_adjust(hspace=.01)
    # x0, x1, y0, y1 = plt.axis()
    # print(x0, x1, y0, y1)
    # plt.axis((x0 - 0,
    #           x1 + 0,
    #           y0 - 2,
    #           y1 + 2))
    plt.savefig(outFile,dpi=320)

if __name__ == '__main__':
    X, col_names, names = get_data()
    create_chart(X, col_names, names,'flav_acc_per_person_reg.png',60.)
