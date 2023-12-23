import os
import sys
import pandas as pd
import numpy as np
import art
from tqdm import tqdm

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# add modules path if this file is launched as __main__
#------------------------------------------------------------------------------
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# import modules and classes
#------------------------------------------------------------------------------
from modules.components.data_classes import UserOperations, SurvivalAnalysis
from modules.components.plot_classes import PlotBoard
import modules.global_variables as GlobVar
import modules.configurations as cnf

# [SURVIVAL ANALYSIS]
#==============================================================================
# ...
#==============================================================================
operator = UserOperations()
plotworker = PlotBoard()
survival = SurvivalAnalysis()

# load data
#------------------------------------------------------------------------------
filepath = os.path.join(GlobVar.data_path, f'{cnf.filename}.csv')                
df_survival = pd.read_csv(filepath, sep= ';', encoding='utf-8')

# Select columns for survival curves
#------------------------------------------------------------------------------
print(''' 
------------------------------------------------------------------------------- 
SURVIVAL ANALYSIS: KAPLAN-MEIER CURVES 
-------------------------------------------------------------------------------
Select the target columns to perform survival analysis. The following columns
have been found in the dataset:
-------------------------------------------------------------------------------
''')
for id, col in enumerate(df_survival.columns):
    print(f'{id + 1} - {col}')
print()
while True:
    try:
        treatment_col = int(input('Select the patient treatment (grouping) column: '))               
    except:
        continue            
    while treatment_col not in range(df_survival.shape[1]):
        try:
            treatment_col = int(input('Input is not valid, please select a valid option: '))                    
        except:
            continue
    break

while True:    
    event_cols = input('Select the event columns (separated by comma): ')
    event_cols = [int(col) for col in event_cols.split(',')]             
    while all(col in range(df_survival.shape[1]) for col in event_cols):
        break
    else:
        event_cols = input('Input is not valid, please select a valid option: ')
        event_cols = [int(col) for col in event_cols.split(',')]
    break

while True:    
    time_cols = input('Select the time columns (separated by comma): ')
    time_cols = [int(col) for col in time_cols.split(',')]             
    while all(col in range(df_survival.shape[1]) for col in time_cols):
        break
    else:
        time_cols = input('Input is not valid, please select a valid option: ')
        time_cols = [int(col) for col in time_cols.split(',')]
    break

# generate redux version of the dataset based on column selection
#------------------------------------------------------------------------------
selected_columns = [treatment_col] + event_cols + time_cols
selected_columns = [x - 1 for x in selected_columns]
df_survival_redux = df_survival.iloc[:, selected_columns]

# check presence of null values
#------------------------------------------------------------------------------
null_values = df_survival_redux.isnull().sum()
df_survival_redux = df_survival_redux.dropna(how='any').astype(float)

print(f'''
-------------------------------------------------------------------------------
OVERVIEW OF DATASET
-------------------------------------------------------------------------------
Number of observations =   {df_survival.shape[0]}
NA values in the dataset = {null_values.max()}
Number of true observation = {df_survival_redux.shape[0]}
-------------------------------------------------------------------------------    
''')

# Generate survival curves (KaplanMeier curves)
#------------------------------------------------------------------------------
for time, event in zip(cnf.survival_times, cnf.survival_events):
    df_KM = df_redux[cnf.treatment_col, time, event]
    survival.KaplanMeier_curves(df_KM, time, event, group_col=cnf.treatment_col, 
                                path=GlobVar.fig_path, filename=f'KM_cumulative_{event}',
                                x_label='Time to event (in days)', y_label= f'{event} probability',
                                inverse=False)
    survival.KaplanMeier_curves(df_KM, time, event, group_col=cnf.treatment_col, 
                                path=GlobVar.fig_path, filename=f'KM_curve_{event}',
                                x_label='Time to event (in days)', y_label= f'{event} probability',
                                inverse=True)

# calculate propensity score and IPTW
# ------------------------------------------------------------------------------
print('''2) - IPTW and COX CURVES
''')

treatment_col = 'is_tx'
covariates = ['rej_any_eFU', 'graft_loss', 'death']
df_survival_redux = survival.IPTW_score(df_survival_redux, covariates, treatment_col)

# split datasets for survival analysis
#------------------------------------------------------------------------------
df_rejection = df_survival_redux[['TT_firstrej', 'rej_any_eFU', 'is_tx', 'IPTW', 'propensity score']]
df_graftloss = df_survival_redux[['TT_graftloss', 'graft_loss', 'is_tx', 'IPTW', 'propensity score']]
df_deceased = df_survival_redux[['TT_death', 'death', 'is_tx', 'IPTW', 'propensity score']]

# Generate survival curves (COX curves)
#------------------------------------------------------------------------------
# survival.CoxPH_curves(df_rejection, 'TT_firstrej', 'rej_any_eFU', group_col='is_tx', 
#                       path=GlobVar.fig_path, filename='Rejection_COX', weight_col='IPTW',
#                       x_label='Time to event (in days)', y_label='Probability of not having a rejection')                     
# survival.CoxPH_curves(df_graftloss, 'TT_graftloss', 'graft_loss', group_col='is_tx', 
#                       path=GlobVar.fig_path, filename='Graftloss_COX', weight_col='IPTW',
#                       x_label='Time to event (in days)', y_label='Probability of not having graft loss')                     
# survival.CoxPH_curves(df_deceased, 'TT_death', 'death', group_col='is_tx', 
#                       path=GlobVar.fig_path, filename='Deceased_COX', weight_col='IPTW',
#                       x_label='Time to event (in days)', y_label='Probability of survival')



# [SAVE FILES]
#==============================================================================
# ...
#==============================================================================

# save csv files
#------------------------------------------------------------------------------
file_loc = os.path.join(GlobVar.save_path, 'TRANSPLANT_processed.csv')    
df_survival_redux.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')


