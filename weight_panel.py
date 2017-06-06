import pandas as pd
import numpy as np

# curr_Month = 2

def get_panel_attendance():
    df = pd.read_excel('data/Bigslip01.Sensory.dbo.CS_SENSORY_ATTENDANCE.xlsx', header=0)
    df = df.dropna()

    #Seperating curr. previous month from all prior previous months
    curr_Month = df.iloc[0,2]
    prior_month_start_idx = np.where(df['att_month']!=curr_Month)[0][0]
    names_list = df.iloc[:prior_month_start_idx,3].as_matrix()
    names_used_list = remove_unused(names_list,df)
    df2 = make_attendance_df(names_used_list,df,prior_month_start_idx)
    return df2, names_used_list

def remove_unused(names_list,df):
    mask = []
    for name in names_list:
        #See if particular name has attended ANY panels
        if np.where((df['n'] ==name) & (df['c'] !=0))[0].shape[0] > 0:
            mask.append(True)
        else:
            mask.append(False)
    mask = np.array(mask)
    return names_list[mask]

def make_attendance_df(names_used_list,df,prior_month_start_idx):
    df_curr = df.iloc[:prior_month_start_idx,:]
    curr_att_per = np.empty_like(names_used_list)
    for x,name in enumerate(names_used_list):
        idx = np.where(df_curr['n']==name)[0][0]
        curr_att_per[x] = (df_curr.iloc[idx,4] / float(df_curr.iloc[idx,5]))

    df_prior = df.iloc[prior_month_start_idx:,:]
    prior_att_per = np.empty_like(names_used_list)
    for x,name in enumerate(names_used_list):
        idx_list = np.where(df_prior['n']==name)[0]
        if idx_list.shape[0] > 0:
            total_attended = 0
            total_possible = 0
            for idx in idx_list:
                total_attended += df_prior.iloc[idx,4]
                total_possible += df_prior.iloc[idx,5]
            prior_att_per[x] = (total_attended / float(total_possible))
        else:
            prior_att_per[x] = 0

    cols = ['name','cur_panel_att','prev_panel_att']
    stacked = np.column_stack((names_used_list,curr_att_per,prior_att_per))
    df_new = pd.DataFrame(stacked,columns=cols)
    return df_new

def get_training_attendance(df,names_used_list):
    df2 = pd.read_excel('data/training_att.xlsx')
    # t = pd.tslib.Timestamp.now()
    # curr_Month = t.month
    # curr_Year = t.year
    ## for testing since data not current
    curr_Month = 2
    curr_Year = 2017
    dfa = df2.loc[df2['Attendance Type ']=='Expert Taste Panel Training']
    curr_idx = np.where((dfa['Date'].map(lambda x: (x.month)==2)) & (dfa['Date'].map(lambda x: (x.year)==2017)))[0][0]
    curr_num = _get_curr_num(dfa,curr_Month,curr_Year)
    print(curr_num)

    df_curr = dfa.iloc[curr_idx:,:]
    curr_att_per = np.empty_like(names_used_list)
    for x,name in enumerate(names_used_list):
        idx_list = np.where(df_curr['Name']==name)[0]
        curr_att_per[x] = idx_list.shape[0] / float(curr_num)

    prior_num = dfa['Date'].nunique() - curr_num
    df_prior = dfa.iloc[:curr_idx,:]
    prior_att_per = np.empty_like(names_used_list)
    for x,name in enumerate(names_used_list):
        idx_list = np.where(df_prior['Name']==name)[0]
        prior_att_per[x] = idx_list.shape[0] / float(prior_num)

    col_list = list(df.columns)
    col_list.extend(('curr_train_att','prior_train_att'))
    X = df.values
    stacked = np.column_stack((X,curr_att_per,prior_att_per))
    df_new = pd.DataFrame(stacked,columns=col_list)
    return df_new

def _get_curr_num(dfa,curr_Month,curr_Year):
    d = dfa['Date'].unique()
    d = pd.DataFrame(d)
    num = d.loc[(d[0].map(lambda x: x.month)==curr_Month) & (d[0].map(lambda x: x.year)==curr_Year)].shape[0]
    return num



if __name__ == '__main__':
    df,names_used_list = get_panel_attendance()
    df = get_training_attendance(df,names_used_list)
