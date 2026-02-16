####################################################################################################################################
#################################################### [DO NOT CHANGE THIS CODE] #####################################################
####################################################################################################################################

## import libraries
import os
import pandas as pd
from parameters import *

## Load the data (CSV files in the input folder) and create the output folders [DO NOT CHANGE, ONLY CHANGE IN THE PARAMETERS ABOVE]
sas_output = {}
path = os.getcwd()
for root, dirs, files in os.walk(f'{path}/{input_folder}'):
    for file in files:
        if file.endswith('.csv'):
            try:
                sas_output[file.split('.')[0]] = pd.read_csv(f'{root}/{file}', sep = delimiter)
            except:
                raise Exception(f'\n\nError reading the input files. Please check the delimiter in the parameters.py file.\n')

if not sas_output:
    raise Exception(f"\n\nERROR: No CSV files found in the input folder. Please check the folder <{input_folder}> in the root directory.\n")

# Create folders for the plots (do not change!)
plots = ['PD', 'LGD', 'EAD', 'ECL', 'Staging', 'Others']     # plots to be generated

for plot in plots:
    if not os.path.exists(newfolder + '/plots/' + plot):
        os.makedirs(newfolder + '/plots/' + plot)
