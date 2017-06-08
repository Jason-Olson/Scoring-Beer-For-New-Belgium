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

def create_chart(X, col_names, names,outFile):
    fig, axes = plt.subplots(ncols=1, nrows=int(len(col_names)/2),figsize=(120,120))#,figsize=(200,100)
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
        ax.set_ylabel(col_names[xi][:col_names[xi].find('_')],fontsize=20)
        ax.set_ylim(0., 60.)
        if i ==int(len(col_names)/2-1):
            ax.set_xticks(x_axis)
            ax.set_xticklabels(names,rotation='vertical')
        else:
            ax.tick_params(
                            axis='x',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            bottom='off',      # ticks along the bottom edge are off
                            top='off',         # ticks along the top edge are off
                            labelbottom='off')

    plt.tight_layout()
    plt.savefig(outFile)

if __name__ == '__main__':
    X, col_names, names = get_data()
    create_chart(X, col_names, names,'flav_acc_per_person.png')
