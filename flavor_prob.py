import spacy
import pandas as pd
import numpy as np
import pickle


def create_flavor_dictionary():
    dfflav = pd.read_excel('data/flavor_description_worksheet.xlsx',header=None)
    Xf = dfflav.values
    nlp = spacy.load('en')
    #drop TTB from list
    Xf = np.delete(Xf,42,axis=0)
    flav_dict = {}
    for x in Xf:
        lem_word = lemmatize_words(nlp,x[1])
        flav_dict[x[0]] = [lem_word]
        for y in range(2,Xf.shape[1]):
            if type(x[y])==str:
                lem_word = lemmatize_words(nlp,x[y])
                flav_dict[x[0]].append(lem_word)
    with open('data/flav_dict.pickle', 'wb') as handle:
        pickle.dump(flav_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return flav_dict

def lemmatize_words(nlp,words):
    tok_list = []
    doc = nlp(str(words))
    for w in doc:
        tok_list.append(w.lemma_)
    lem_word = " ".join(tok_list)
    return lem_word

def flav_dict_from_pickle():
    with open('data/flav_dict.pickle', 'rb') as handle:
        flav_dict = pickle.load(handle)
    return flav_dict

def score_flavor(df,flav_dict):
    X = df[['cClarity', 'cAroma', 'cFlavor', 'cMouthfeel', 'cFresh',
            'cNotFresh']].values
    nlp = spacy.load('en')

    out_list = []
    for i in range(X.shape[0]):
        #Leave th Fresh comments out of this
        text = str(X[i,0]) + str(X[i,1]) + str(X[i,2]) + str(X[i,3]) + str(X[i,5])
        lemm_text = lemmatize_words(nlp,text)
        score_dict={}
        #5for matching key. 2.5 for matching value.
        for key in flav_dict:
            score = 0
            ix = 0
            while text.find(key,ix)!= -1:
                score +=5
                ix = text.find(key,ix) + 1
            for val in flav_dict[key]:
                ix = 0
                while text.find(val,ix)!= -1:
                    score +=2.5
                    ix = text.find(val,ix) + 1
            score_dict[key] = score
        out_list.append(score_dict)
    # get percentage chance for each individual
    for i in range(len(out_list)):
        used_dict={k:v for k,v in out_list[i].items() if v > 0}
        if len(used_dict)!=0:
            sum_of_dict = sum(out_list[i].values())
            p_used_dict = {k:v/float(sum_of_dict) for k,v in used_dict.items()}
            out_list[i] =p_used_dict
        else:
            out_list[i] = {'could not translate comments':1}

    df['flav_dict']= out_list
    return df

if __name__ == '__main__':
    # flav_dict = create_flavor_dictionary()
    flav_dict = flav_dict_from_pickle()
    df = pd.read_pickle('data/joined_results.pickle')
    df = df[df['correct']==1]
    df = score_flavor(df,flav_dict)
