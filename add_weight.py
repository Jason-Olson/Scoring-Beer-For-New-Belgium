import pandas as pd
import numpy as np
import pickle


def add_weight_df(df):
    #get rid of unvalidated and spike data
    df = df[df['isValidated']!=0]
    ## Uncomment if not testing (test data came from spikes)
    # df = df[df['TestType'].str.lower() == 'pr']
    # df = df.loc[-df['Package'].str.lower().isin(['spike','s','ss'])]

    dfng = pd.read_pickle('data/name_group.pickle')

    dfjoin = pd.merge(df,dfng,on=['name'],how='left')
    X = dfjoin['group'].values
    #if some weren't in list
    X[np.where(X==0)]=1
    sum_of = X.sum()
    X = X/ float(sum_of)
    dfjoin['weight'] = X
    dfjoin = dfjoin.drop('group',axis=1)
    return dfjoin



if __name__ == '__main__':
    df = pd.read_pickle('data/joined_results.pickle')
    dfco = df[df['correct']==1]
    dfttb = df[df['mcFresh']==1]
    dfttb= dfttb.sample(10)
    df = pd.concat([df,dfttb])
    print(df.shape)
    df = add_weight_df(df)
