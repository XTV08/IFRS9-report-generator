###################################################################################
###################### [USER PARAMETERS] (ADJUST AS NEEDED) #######################
###################################################################################

## Note: - All folders and files must be in the same directory/folder as the script.
##       - Make sure the file names are in the order of {test}_{model}_{stage}_{weight}_{sub-level}.csv (e.g. backtest_pit_PD_st1_nw_mortgage.csv). Leave {...} empty if not applicable, i.e. no stage, or sub-level.

###################################################################################
############################# [MANUAL INPUT REQUIRED] #############################
###################################################################################

## portfolio type (IMPORTANT)
portfolio_type = 'Retail'                     # portfolio type ('Retail' or 'Wholesale'/'SME') [critical!]

## directory and file names (IMPORTANT)
input_folder = 'input_data'                 # folder containing the input data (e.g. 'input_data') [critical!]
newfolder = r'OutputFolder'                 # create a new folder for the outputs (e.g. r'TestFolder') [critical!]
output_filename = 'IFRS9 Output.xlsx'       # to be generated output Excel file name (e.g. 'IFRS9 Output.xlsx') [critical!]

delimiter = ';'                             # delimiter used in the input CSV files (e.g. ';' or ',') [critical!]

###################################################################################
############################# [MANUAL INPUT OPTIONAL] #############################
###################################################################################

## plot parameters (adjust as needed)
## NOTE: if any plot is not generated while the plot parameters are set correctly, please check whether the specific horizon is present in the data
show_plots = False                  # show plots in the console  (True/False)
sublevel_in_title = True            # include sublevel (sub-models/products/etc.) in the title of the plots (True/False)

## output settings (adjust as needed)
INCLUDE_TABLES = True               # generate tables (True/False)
INCLUDE_PLOTS = True                # generate plots (True/False) (set equal to False if plots are already generated to save time, this will also result in SAS tables not showing up in the Excel file (Cell B3))

INCLUDE_PD = True                   # include PD data in the output Excel file (True/False)
INCLUDE_STAGING = True              # include Staging data in the output Excel file (True/False)
INCLUDE_LGD = True                  # include LGD data in the output Excel file (True/False)
INCLUDE_EAD = True                  # include EAD data in the output Excel file (True/False)
INCLUDE_ECL = True                  # include ECL data in the output Excel file (True/False)
INCLUDE_OTHERS = True               # include other data (not used in certain activities) in the output Excel file (True/False)

## settings for the tables/plots to be generated, this should already be aligned with the current activity requirements
## and do not need to be changed (otherwise, adjust as needed)
# number-weighted or exposure-weighted for each parameter
PD_weight = ['nw', 'ew']            # weight for PD plot (ew/nw) (e.g. ['nw', 'ew'] or ['ew'])
LGD_weight = ['ew']                 # weight for LGD plot (ew/nw)
EAD_weight = ['ew']                 # weight for EAD plot (ew/nw)
ECL_weight = ['ew']                 # weight for ECL plot (ew/nw)
PSI_weight = ['nw', 'ew']           # weight for PSI plot (ew/nw)
cure_weight = ['nw']                # weight for cure/no loss rate plot (nw/ew)

# horizons to consider for each parameter
PD_horizons = [0, 1, 2, 3, 4]       # horizons for PD plot (e.g. [0, 1, 2, 3, 4] or [0])
STAGING_horizons = [0]              # horizons for Staging plot (e.g. [0, 1, 2, 3, 4] or [0])
LGD_horizons = [0, 1, 2, 3, 4]      # horizons for LGD plot (e.g. [0, 1, 2, 3, 4] or [0])
EAD_horizons = [0, 1, 2, 3, 4]      # horizons for EAD plot (e.g. [0, 1, 2, 3, 4] or [0])
ECL_horizons = [0, 1, 2, 3, 4]      # horizons for ECL plot (e.g. [0, 1, 2, 3, 4] or [0])

# stages to consider for each parameter
PD_stages = [1, 2]                  # stages for PD plot (e.g. [1, 2] or [1])
LGD_stages = [1, 2, 'indef']        # stages for LGD plot (e.g. [1, 2, 'indef'] or [1])
ECL_stages = [1, 2]                 # stages for ECL plot (e.g. [1, 2] or [1])


