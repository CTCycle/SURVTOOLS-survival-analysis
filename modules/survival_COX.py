import os
import pandas as pd
import numpy as np
import art
from tqdm import tqdm

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------
from modules.components.data_classes import SurvivalAnalysis
from modules.components.plot_classes import PlotBoard
import modules.global_variables as GlobVar
import modules.configurations as cnf

# welcome message
#------------------------------------------------------------------------------
ascii_art = art.text2art('SURVTOOLS')
print(ascii_art)

# [PRELIMINARY DATA PROCESSING]
#==============================================================================
# ...
#==============================================================================

# load data and replace n.a. with numpy NaN
#------------------------------------------------------------------------------
filepath = os.path.join(GlobVar.data_path, f'{cnf.filename}.csv')                
df_survival = pd.read_csv(filepath, sep= ';', encoding='utf-8')



# [SURVIVAL ANALYSIS]
#==============================================================================
# ...
#==============================================================================
plotworker = PlotBoard()
survival = SurvivalAnalysis()

print('''
      
SURVIVAL ANALYSIS
-------------------------------------------------------------------------------
Generate Kaplan-Meier curves for the given dataset. As a second step, calculate the
propensity score for the treatments groups, and apply the score to COX survival curves
------------------------------------------------------------------------------- 
    
''')

# redux the dataset for survival analysis
#------------------------------------------------------------------------------
survival_cols = ['is_tx', 'TT_firstrej', 'rej_any_eFU', 
                 'TT_graftloss', 'graft_loss',
                 'TT_death', 'death']

df_survival = df_transplant[survival_cols]
df_survival = df_survival[df_survival['is_tx'] != 2]
null_values = df_survival.isnull().sum()
df_survival_redux = df_survival.dropna(how='any')
df_survival_redux = df_survival_redux.astype(float)

print(f'''
OVERVIEW
-------------------------------------------------------------------------------
Number of observations =   {df_survival.shape[0]}
NA values in the dataset = {null_values.max()}
Number of true observation = {df_survival_redux.shape[0]}
-------------------------------------------------------------------------------    

1) - KAPLAN-MEIER SURVIVAL CURVES

''')

# split datasets for survival analysis
#------------------------------------------------------------------------------
df_rejection = df_survival_redux[['TT_firstrej', 'rej_any_eFU', 'is_tx']]
df_graftloss = df_survival_redux[['TT_graftloss', 'graft_loss', 'is_tx']]
df_deceased = df_survival_redux[['TT_death', 'death', 'is_tx']]

# Generate survival curves (KaplanMeier curves)
#------------------------------------------------------------------------------
survival.KaplanMeier_curves(df_rejection, 'TT_firstrej', 'rej_any_eFU', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Rejection_KPM',
                            x_label='Time to event (in days)', y_label='Probability of not having a rejection',
                            inverse=False)
survival.KaplanMeier_curves(df_graftloss, 'TT_graftloss', 'graft_loss', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Graftloss_KPM',
                            x_label='Time to event (in days)', y_label='Probability of not having graft loss',
                            inverse=False)
survival.KaplanMeier_curves(df_deceased, 'TT_death', 'death', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Deceased_KPM',
                            x_label='Time to event (in days)', y_label='Probability of survival',
                            inverse=False)

# Generate survival curves (KaplanMeier curves, cumulative)
#------------------------------------------------------------------------------
survival.KaplanMeier_curves(df_rejection, 'TT_firstrej', 'rej_any_eFU', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Rejection_KPM_cumulative',
                            x_label='Time to event (in days)', y_label='Probability of organ rejection',
                            inverse=True)
survival.KaplanMeier_curves(df_graftloss, 'TT_graftloss', 'graft_loss', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Graftloss_KPM_cumulative',
                            x_label='Time to event (in days)', y_label='Probability of having graft loss',
                            inverse=True)
survival.KaplanMeier_curves(df_deceased, 'TT_death', 'death', group_col='is_tx', 
                            path=GlobVar.fig_path, filename='Deceased_KPM_cumulative',
                            x_label='Time to event (in days)', y_label='Probability of death',
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


