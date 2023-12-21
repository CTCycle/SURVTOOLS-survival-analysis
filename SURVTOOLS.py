import sys
import art

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------
from modules.components.data_classes import UserOperations

# welcome message
#------------------------------------------------------------------------------
ascii_art = art.text2art('SURVTOOLS')
print(ascii_art)

# [MAIN MENU]
#==============================================================================
# module for the selection of different operations
#==============================================================================
user_operations = UserOperations()
operations_menu = {'1' : 'Generate Kaplan-Meier survival curves',
                   '2' : 'Generate COX survival curves',                                                                    
                   '3' : 'Exit and close'}

while True:
    print('------------------------------------------------------------------------')    
    op_sel = user_operations.menu_selection(operations_menu)
    print()     
    if op_sel == 1:
        import modules.survival_KM
        del sys.modules['modules.survival_KM']
    elif op_sel == 2:
        import modules.survival_COX
        del sys.modules['modules.survival_COX']
    elif op_sel == 3:
        break


