import pandas as pd
import numpy as np
import pickle
import requests
import json


def convert_data_and_return_pred(df,bnb_d,bnb_od_p,bnb_od_r,tf_d,tf_od_p,tf_od_r,rf_mod):
    unpack_tix(df)
    previous_payouts(df)
    add_cols(df,bnb_d,bnb_od_p,bnb_od_r,tf_d,tf_od_p,tf_od_r)
    trim_df(df)
    df.fillna(0)
    X =  df.values
    df['fraud'] = rf_mod.predict(X)
    df['priority'] = df.apply(add_priority,axis=1)
    return df

def add_priority(row):
    # # average cost of 200 is 75%, 475 = 90%, high priority above that for 10% of fraud detected
    ## 0 = not fraud, 1 = low, 2 = med., 3 = high
    if row['fraud']:
        if row['avg_cost'] <= 200:
            return 1
        elif row['avg_cost'] <= 475:
            return 2
        else:
            return 3
    else:
        return 0

def unpack_tix(df): # ticket column is a list of dictionaries of unicode; we want that information pulled out into separate columns for analysis
    cost = [] # create empty lists
    quantity_sold = []
    quantity_total = []

    for i in range(len(df['ticket_types'])): # all rows
        line_cost = [] # reset values for new row
        line_quant = []
        line_total = []
        for j in range(len(df['ticket_types'].values[i])): # each separate listing per row
            line_cost.append(df['ticket_types'].values[i][j]['cost']) # add to row list
            line_quant.append(df['ticket_types'].values[i][j]['quantity_sold'])
            line_total.append(df['ticket_types'].values[i][j]['quantity_total'])
        cost.append(line_cost) # add row list to full list
        quantity_sold.append(line_quant)
        quantity_total.append(line_total)

    df['cost'] = cost # set lists as new df columns
    df['quantity_sold'] = quantity_sold
    df['quantity_total'] = quantity_total

def previous_payouts(df):
    n = len(df['previous_payouts'])
    n_previous_transactions = []
    user_id = []
    user_state = []
    previous_amounts = [[] for x in range(n)]

    for i in range(n):
        lis = df['previous_payouts'].iloc[i]
        n_previous_transactions.append(len(lis))
        try:
            user_id.append(lis[0]['uid'])
        except:
            user_id.append(np.nan)
        try:
            user_state.append(lis[0]['state'])
        except:
            user_state.append(np.nan)
        for entry in lis:
            previous_amounts[i].append(entry['amount'])
    df['n_previous_transactions'] = n_previous_transactions
    df['user_id'] = user_id
    df['user_state'] = user_state
    df['previous_amounts'] = previous_amounts

def trim_df(df):
    trim = ['approx_payout_date', 'org_name', 'payout_type', 'payee_name', 'org_desc', 'num_payouts', 'num_order', 'name', 'object_id', 'user_id', 'venue_latitude', 'venue_longitude', 'venue_state', 'venue_address', 'venue_country', 'venue_name', 'cost', 'listed', 'has_header', 'country', 'email_domain', 'event_created', 'event_end', 'event_published', 'event_start', 'description', 'currency', 'gts', 'previous_payouts', 'ticket_types', 'previous_amounts', 'quantity_sold', 'quantity_total', 'user_created', 'user_state']

    for col in trim:
        df.pop(col)

def add_cols(df,bnb_d,bnb_od_p,bnb_od_r,tf_d,tf_od_p,tf_od_r):
    # listed
    df['listed'] = [1 if x == 'y' else 0 for x in df['listed']]
    # avg_amounts
    avg_amounts = []
    for entry in df['previous_amounts']:
        if len(entry) != 0:
            avg_amounts.append(float(sum(entry))/len(entry))
        else:
            avg_amounts.append(0)
    df['avg_amounts'] = avg_amounts
    # avg_cost
    avg_cost = []
    for entry in df['cost']:
        if len(entry) != 0:
            avg_cost.append(float(sum(entry))/len(entry))
        else:
            avg_cost.append(0)
    df['avg_cost'] = avg_cost
    ##For probas

    # if df.shape[0] == 1:
    #     df['description_proba'] = bnb_d.predict_proba(tf_d.transform(df['description']))[1]
    #     df['org_description_proba_r'] = bnb_od_r.predict_proba(tf_od_r.transform(df['description']))[1]
    #     df['org_description_proba_p'] = bnb_od_p.predict_proba(tf_od_p.transform(df['description']))[1]
    # else:
    df['description_proba'] = bnb_d.predict_proba(tf_d.transform(df['description']))[:,1]
    df['org_description_proba_r'] = bnb_od_r.predict_proba(tf_od_r.transform(df['description']))[:,1]
    df['org_description_proba_p'] = bnb_od_p.predict_proba(tf_od_p.transform(df['description']))[:,1]

    # peter's states
    df['diff_state'] = check_location(df)

    # 0 means same state or NaN, 1 means CLEARLY different state

def check_location(df): # comparing 'venue_state' vs. 'user_state' to identify observable differences
    schtuff = []
    if df.shape[0] > 1:
        for i in range(len(df)):
            if df['venue_state'][i] == 'nan' or df['user_state'][i] == 'nan':
                schtuff.append(0)
            elif df['venue_state'][i] == df['user_state'][i]:
                schtuff.append(0)
            elif df['venue_state'][i] != df['user_state'][i]:
                schtuff.append(1)
    else:
        if df['venue_state'].values[0] == 'nan' or df['user_state'].values[0] == 'nan':
            schtuff.append(0)
        elif df['venue_state'].values[0] == df['user_state'].values[0]:
            schtuff.append(0)
        elif df['venue_state'].values[0] != df['user_state'].values[0]:
            schtuff.append(1)
    return schtuff

def unpickle_models(file_p):
    with open(file_p, 'rb') as handle:
        temp = pickle.load(handle)
    return temp

if __name__ == '__main__':
    new_data = requests.get('http://galvanize-case-study-on-fraud.herokuapp.com/data_point').text
    nd_j = json.loads(new_data)
    df = pd.DataFrame.from_dict(nd_j, orient='index').T

    bnb_d = unpickle_models('pickles/bnb.pickle')
    bnb_od_p = unpickle_models('pickles/bnb_org_desc.pickle')
    bnb_od_r = unpickle_models('pickles/bnb_org_desc_rec.pickle')
    tf_d = unpickle_models('pickles/tf.pickle')
    tf_od_p = unpickle_models('pickles/tf_org_desc.pickle')
    tf_od_r = unpickle_models('pickles/tf_org_desc_rec.pickle')
    rf_mod = unpickle_models('pickles/randomforest_fraud.pickle')


    df2 = convert_data_and_return_pred(df,bnb_d,bnb_od_p,bnb_od_r,tf_d,tf_od_p,tf_od_r,rf_mod)
