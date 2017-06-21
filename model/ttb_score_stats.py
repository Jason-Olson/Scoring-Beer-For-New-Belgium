import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.close('all')

def get_data():
    df = pd.read_pickle('data/full_run.pickle')
    return df

def get_summary(df):
    ###
    # In:__ A dataframe with the results obtained from df_results
    #
    # Out:__ A dictionary with key being "TTB", "Not TTB but uncertain why", or the flavor, and value being a list
    #        containing the probabilites appearing in all the different brew numbers ran.
    ###

    X = df['results_dict'].values

    out_dict = {}
    for x in X:
        for tup in x:
            k = tup[0]
            v = tup[1]
            _add_to_out_dict(out_dict,k,v)
    return out_dict

def _add_to_out_dict(out_dict,k,v):
        if k not in out_dict.keys():
            out_dict[k] = [v]
        else:
            out_dict[k].append(v)
        return out_dict

def generate_ttb_histogram(out_dict):
    #comment on/off in main
    ttb_a = np.array(out_dict['TTB'])
    plt.hist(ttb_a,bins = 'auto')
    plt.title("TTB Histogram")
    plt.savefig('graphs/ttb_hist.png')

def remove_outliers(out_dict):
    ttb_a = np.array(out_dict['TTB'])
    fq = np.percentile(ttb_a,25)
    tq = np.percentile(ttb_a,75)
    iqr = tq - fq
    out_mark = fq - (iqr * 1.5)
    ttb_out = np.delete(ttb_a,np.where(ttb_a <= out_mark)[0])
    return ttb_out

def get_cut_threshold(ttb_out):
    #In:  np.array with outliers removed by remove_outliers
    median = np.median(ttb_out)
    std_dev = ttb_out.std()
    return (median - (3* std_dev))*100

if __name__ == '__main__':
    df = get_data()
    out_dict = get_summary(df)
    # generate_ttb_histogram(out_dict)
    ttb_out = remove_outliers(out_dict)

    print('Any TTB score less than {} is considered "out of control" and should be investigated'.format(str(round(get_cut_threshold(ttb_out),2))))
