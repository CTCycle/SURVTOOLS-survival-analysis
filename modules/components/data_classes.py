import os
import numpy as np
import statsmodels.api as sm
import lifelines as lf
import matplotlib.pyplot as plt



# ...
#==============================================================================
#==============================================================================
#==============================================================================
class UserOperations:
    
    
    #==========================================================================    
    def menu_selection(self, menu):
        
        '''         
        Prompts a selection menu using a dictionary as reference, allows the user to
        select one option and returns the selection preference         
        
        Keyword arguments:
            menu (dict): dictionary containing multiple menu options
        
        Returns:                
            op_sel (int): integer representing the selection reference
        
        '''        
        indexes = [idx + 1 for idx, val in enumerate(menu)]
        for key, value in menu.items():
            print(f'{key} - {value}')            
        print()     
        while True:
            try:
                op_sel = int(input('Select the desired operation: '))                
            except:
                continue            
            while op_sel not in indexes:
                try:
                    op_sel = int(input('Input is not valid, please select a valid option: '))                    
                except:
                    continue
            break
        
        return op_sel
    
    
    


# ...
#==============================================================================
#==============================================================================
#==============================================================================
class SurvivalAnalysis:

    #==========================================================================
    def IPTW_score(self, df, covariates_cols, target_col):
        
        covariates = df[covariates_cols]              
        logit_model = sm.Logit(df[target_col], covariates)
        result = logit_model.fit()           
        df['propensity score'] = result.predict(covariates)
        df['IPTW'] = np.where(df[target_col] == 1, 1/df['propensity score'], 1/(1 - df['propensity score']))
        df['IPTW'] = df['IPTW'].apply(lambda x : round(x, 5))

        return df

    #==========================================================================
    def KaplanMeier_curves(self, df, time_col, event_col, path, 
                           filename, x_label, y_label, group_col=None,
                           inverse=False):
        
        kmf = lf.KaplanMeierFitter()
        ax = plt.subplot(111) 
        if group_col is not None:
            for group in df[group_col].unique():
                time = df.loc[df[group_col] == group, time_col]
                event = df.loc[df[group_col] == group, event_col]
                kmf.fit(time, event, label=str(group))            
                if inverse == True: 
                    kmf.plot_cumulative_density(ax=ax)
                else:
                    kmf.plot_survival_function(ax=ax)                
        else: 
            time = df[time_col]
            event = df[event_col]
            kmf.fit(time, event)          
            if inverse == True: 
                kmf.plot_cumulative_density(ax=ax)
            else:
                kmf.plot_survival_function(ax=ax)            
                    
        plt.xlabel(x_label)
        plt.ylabel(y_label)       
        plot_loc = os.path.join(path, '{}.jpeg'.format(filename))
        plt.tight_layout()
        plt.savefig(plot_loc, bbox_inches='tight', format='jpeg', dpi=600)        
        plt.close()

    #==========================================================================       
    def CoxPH_curves(self, df, time_col, event_col, path, filename, x_label,
                     y_label, weight_col, group_col):
        

        cph = lf.CoxPHFitter()       
        ax = plt.subplot(111)         
        for group in df[group_col].unique():            
            df_group = df[df[group_col] == group]                      
            cph.fit(df_group, duration_col=time_col, event_col=event_col, weights_col=weight_col)         
            cph.plot_partial_effects_on_outcome(ax=ax)
        plt.xlabel(x_label)
        plt.ylabel(y_label)       
        plot_loc = os.path.join(path, '{}.jpeg'.format(filename))
        plt.tight_layout()
        plt.savefig(plot_loc, bbox_inches='tight', format='jpeg', dpi=600)        
        plt.close()
            
       
    
