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
    df = column_name_prep(df)
    dfjoin = pd.merge(df,dfng,on=['name'],how='left')
    #if some weren't in list
    dfjoin = dfjoin.replace(np.nan, 1)
    X = dfjoin['group'].values
    sum_of = X.sum()
    X = X/ float(sum_of)
    dfjoin['weight'] = X
    dfjoin = dfjoin.drop('group',axis=1)
    return dfjoin

def column_name_prep(df):
    df['RegName'] = df['RegName'].str.lower()
    df['RegName'] = df['RegName'].replace('billy bletcher','bill bletcher')
    df['RegName'] = df['RegName'].replace('matty gilliland','matt gilliland')
    df['RegName'] = df['RegName'].replace('philip pollick','phil pollick')
    new_cols = list(df.columns)
    new_cols = [w.replace('RegName','name') for w in new_cols]
    df.columns = new_cols
    return df



if __name__ == '__main__':
    df = pd.read_pickle('data/joined_results.pickle')
    #just to make example work
    new_cols = list(df.columns)
    new_cols = [w.replace('name','RegName') for w in new_cols]
    df.columns = new_cols
    ##
    dfco = df[df['correct']==1]
    dfttb = df[df['mcFresh']==1]
    dfttb= dfttb.sample(10)
    df = pd.concat([df,dfttb])

    df = add_weight_df(df)
