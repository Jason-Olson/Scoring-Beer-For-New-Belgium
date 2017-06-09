import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


def get_data():
    # df = pd.read_pickle('data/joined_results.pickle')
    # df = df.replace(np.nan, '', regex=True)
    # X = df[['cClarity', 'cAroma', 'cFlavor', 'cMouthfeel', 'cFresh',
    #             'cNotFresh', 'mcClarity', 'mcAroma', 'mcFlavor', 'mcMouthfeel',
    #             'mcFresh']].values
    # y = df['correct'].values
    X = np.load('data/Xarr.npy')
    y = np.load('data/yarr.npy')

    return X,y



if __name__ == '__main__':
    X,y= get_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    cv_list=[]
    for i in range(6):
        X_t = X_train[:,i]
        X_t = X_t.flatten()
        cv = CountVectorizer(lowercase=False)
        x_tran = cv.fit_transform(X_t)
        cv_list.append(cv)
        xarr = x_tran.toarray()
        X_train = np.column_stack((X_train,xarr))
        # for k in range(X.shape[0]):
        #     X[k,i] = xarr[k,:].reshape(1,xarr.shape[1])
    X_train = X_train[:,6:]

    for i in range(6):
        X_t = X_test[:,i]
        X_t = X_t.flatten()
        # cv = CountVectorizer(lowercase=False)
        x_tran = cv_list[i].transform(X_t)
        # cv_list.append(cv)
        xarr = x_tran.toarray()
        X_test = np.column_stack((X_test,xarr))
        # for k in range(X.shape[0]):
        #     X[k,i] = xarr[k,:].reshape(1,xarr.shape[1])
    X_test = X_test[:,6:]



    xgb = XGBClassifier()
    xgb.fit(X_train,y_train)
    y_pred = xgb.predict(X_test)
    print('accuracy score of:  {}'.format(accuracy_score(y_test,y_pred)))
