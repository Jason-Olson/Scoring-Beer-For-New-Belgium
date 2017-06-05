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
    return df2

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

if __name__ == '__main__':
    df = get_panel_attendance()
