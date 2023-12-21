import os

# define paths
#------------------------------------------------------------------------------
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dataset')
save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')    
fig_path = os.path.join(save_path, 'figures')

# create folders from paths
#------------------------------------------------------------------------------
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(save_path):
    os.mkdir(save_path) 
if not os.path.exists(fig_path):
    os.mkdir(fig_path) 


