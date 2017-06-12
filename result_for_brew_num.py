import pandas as pd
import numpy as np
import pickle
from build_model import add_prediction
from flavor_prob import score_flavor


def score_batch(df):
    ###
    # In:__ A dataframe already filtered down to a brew number and conatining the columns
    # ('pred_correct', 'flav_dict') obtained as output from buld_model's add_prediction
    # and flavor_prob's score_flavor scripts respectively.
    #
    # Out:__ A list of tuples ('description',prob) containing the probabilities of being TTB, the 'Flavors' present, or 'Not TTB but uncertain why'
    ###

    '''move to weight function
    df = df[df['format'] != 'spike']
    '''

    #weight functionality to be added soon...Uniform for now
    ###
    df['weight'] = 1.0/df.shape[0]
    X = df[['mcFresh', 'pred_correct', 'flav_dict', 'weight']].values
    mcFresh = 0
    pred_correct = 1
    flav_dict = 2
    weight = 3

    out_dict = {}
    for x in X:
        if x[mcFresh] == 1:
            if 'TTB'  not in out_dict.keys():
                out_dict['TTB'] = x[weight] * 1
            else:
                out_dict['TTB'] += x[weight] * 1
        else:
            row_dict = x[flav_dict]
            for k,v in row_dict.items():
                out_dict = _add_to_out_dict(out_dict,k,v,x)
            out_dict = _add_to_out_dict(out_dict,'Not TTB but uncertain why',(1.0- x[pred_correct]),x)
    out_list = [(k,v) for k,v in out_dict.items()]
    out_list.sort(key= lambda x: x[1],reverse=True)
    return out_list


def _add_to_out_dict(out_dict,k,v,x):
        mcFresh = 0
        pred_correct = 1
        flav_dict = 2
        weight = 3
        if k == 'TTB':
            if k  not in out_dict.keys():
                out_dict[k] = x[weight] * 1
            else:
                out_dict[k] += x[weight] * 1
        elif k == 'Not TTB but uncertain why':
            if k  not in out_dict.keys():
                out_dict[k] = x[weight] * v
            else:
                out_dict[k] += x[weight] * v
        else:
            if k not in out_dict.keys():
                out_dict[k] = x[weight] * (v * x[pred_correct])
            else:
                out_dict[k] += x[weight] * (v * x[pred_correct])
        return out_dict






if __name__ == '__main__':
        # Generate sample data
        df = pd.read_pickle('data/joined_results.pickle')
        dfco = df[df['correct']==1]
        dfttb = df[df['mcFresh']==1]
        dfttb= dfttb.sample(10)
        df = pd.concat([df,dfttb])
        #Run xgboost model to get our confidence in comments score
        df = add_prediction(df)
        #Adds flavor probability dictionary to dataframe
        df = score_flavor(df)
        batch_panel_results = score_batch(df)
