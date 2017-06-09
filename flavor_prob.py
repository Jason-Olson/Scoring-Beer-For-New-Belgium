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
    return flav_dict

def lemmatize_words(nlp,words):
    tok_list = []
    doc = nlp(str(words))
    for w in doc:
        tok_list.append(w.lemma_)
    lem_word = " ".join(tok_list)
    return lem_word

if __name__ == '__main__':
    flav_dict = create_flavor_dictionary()
