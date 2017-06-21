import pickle
import pandas as pd
import numpy as np

def get_data():
    with open('data/names_list2.pickle', 'rb') as handle:
        names_used_list = pickle.load(handle)

    df = pd.read_pickle('data/df_pickle.pickle')

    dfknown = pd.read_pickle('data/training_attribute.pickle')
    dfknown['format'] = dfknown['format'].str.lower()
    dfknown = dfknown.loc[dfknown['format']=='spike']
    dfknown['base beer'] = dfknown['base beer'].str.strip().str.lower()
    dfknown = dfknown.loc[dfknown['base beer'].isin(['fat tire', 'fat tire can'])]
    df['Flavor'] = df['Flavor'].str.lower()
    comment_flav_list=['ft','ft32','ftc','ftc32','ft mv','fat tire','ftwht','ft32abw','ft15','ft-c','ft-t','ft 3 day can','ftc32abw']
    df = df.loc[df['Flavor'].isin(comment_flav_list)]

    df['RegName'] = df['RegName'].str.lower()
    dfknown['Full Name'] = dfknown['Full Name'].str.lower()

    #filter all by names in name_used_list
    df = df[df['RegName'].isin(names_used_list)]
    dfknown = dfknown[dfknown['Full Name'].isin(names_used_list)]

    df['TestType'] = df['TestType'].str.lower()
    df['Package'] = df['Package'].str.lower()
    df = df.loc[(df['Package'].isin(['spike','s','ss'])) | (df['TestType']=='s')]
    df,dfknown = df_replace_names(df,dfknown)
    df,dfknown = common_columns(df,dfknown)
    df = df.drop('p50',axis=1)
    df = df.drop_duplicates()
    dfknown = dfknown.drop_duplicates()

    return df, dfknown, names_used_list

def df_replace_names(df,dfknown):
    df['RegName'] = df['RegName'].replace('billy bletcher','bill bletcher')
    df['RegName'] = df['RegName'].replace('matty gilliland','matt gilliland')
    df['RegName'] = df['RegName'].replace('philip pollick','phil pollick')
    dfknown['Full Name'] = dfknown['Full Name'].replace('billy bletcher','bill bletcher')
    dfknown['Full Name'] = dfknown['Full Name'].replace('matty gilliland','matt gilliland')
    dfknown['Full Name'] = dfknown['Full Name'].replace('philip pollick','phil pollick')
    return df,dfknown

def common_columns(df,dfknown):
    new_cols = list(dfknown.columns)
    new_cols = [w.replace('Full Name','name').replace('Date','date') for w in new_cols]
    dfknown.columns = new_cols

    new_cols = list(df.columns)
    new_cols = [w.replace('RegName','name').replace('SessionDate','date') for w in new_cols]
    df.columns = new_cols
    return df,dfknown


if __name__ == '__main__':
    df, dfknown, names_used_list = get_data()
    dfjoin = pd.merge(dfknown,df,on=['name','date'],how='inner')
    col_list = list(dfjoin.columns)
    X = dfjoin.values
    drop_list = []
    for i in range(X.shape[0]):
        if i != (X.shape[0]-1):
            if (X[i,3] == X[i+1,3]) and (X[i,11] == X[i+1,11]):
                drop_list.append(i)
                drop_list.append(i+1)
    X = np.delete(X, drop_list, axis=0)
    dfjoin = pd.DataFrame(X,columns=col_list)
