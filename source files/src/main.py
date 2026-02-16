#%%
### import libraries
print("\n################################")
print("Importing libraries and files...")
print("################################\n")
import pandas as pd
import numpy as np
import os
import sys

path = os.getcwd()
sys.path.append(path)

from parameters import *    # import the classes from the classes.py file (in the root folder next to the .exe file)
from import_data import *   # import the data using import_data.py (in the src folder)
from classes import *       # import the parameters from the parameters.py file (in the src folder)

## Note: if sublevels (sub-models/products/etc.) are present, make sure the SAS output files don't include _st or _rat in them to define the sublevels (rename in that case),
#        outputs for stages/ratings must include _st or _rat


#######################################################################################################################
#%%
### Initialise dictionaries for all the tables that are generated, including the SAS input tables that were used
## note: all additional tables that are created but not used in a certain activity are stored in the 'others' dictionary
all_tests = ['PD_CQ_1', 'PD_CQ_2', 'PD_CQ_3', 'PD_CQ_4', 'PD_CQ_5', 'PD_CQ_6',
             'STAGING_DP_1', 'STAGING_DP_2', 'STAGING_DP_3', 'STAGING_CQ_1', 'STAGING_CQ_2', 'STAGING_CQ_3', 'STAGING_CQ_4',
             'LGD_CQ_1', 'LGD_CQ_2', 'LGD_CQ_3', 'LGD_CQ_4', 'LGD_CQ_5', 'LGD_CQ_6',
             'EAD_CQ_1', 'EAD_CQ_2', 'ECL_CQ_1', 'ECL_CQ_2', 'ECL_CQ_3',
             'others']

for test in all_tests:
    vars()[test] = {}
    vars()[test + '_tables'] = {}       # the input tables for plots are created in classes.py (using vars()[test + '_plots'] = {})

## The old generator also creates the following tables, but are no longer used in the current activities:
# PD_DP_1 = {}
# PD_STA_1 = {}
# PD_STA_2 = {}
# provisions = {}


#######################################################################################################################
#%%
### Generate the tables
def generate_tables(sas_output, all_tests):
    print("\n####################")
    print("Generating tables...")
    print("####################\n")
    for key in sas_output.keys():
        if ('discrim_power' in key):
            if ('_stage' in key):
                print(key)
                discrim_power_stage_table = DISCRIM_POWER_STAGE_TABLE(key)
                if key == 'discrim_power_stage'  or '_all' in key or '_oall' in key:                # MCC & Type II error portfolio level
                    STAGING_DP_1[len(STAGING_DP_1)] = discrim_power_stage_table.main_output()
                    STAGING_DP_1_tables[len(STAGING_DP_1_tables)] = key

                    delta_mcc_table = DISCRIM_POWER_STAGE_CHANGE_TABLE(key)                         # MCC change over time portfolio level
                    STAGING_DP_3[len(STAGING_DP_3)] = delta_mcc_table.main_output()
                    STAGING_DP_3_tables[len(STAGING_DP_3_tables)] = key
                else:                                                                               # MCC & Type II error sub-model level
                    STAGING_DP_2[len(STAGING_DP_2)] = discrim_power_stage_table.main_output()
                    STAGING_DP_2_tables[len(STAGING_DP_2_tables)] = key
            else:
                print(key)
                discrim_power_table = DISCRIM_POWER_TABLE(key, 'c_stat')
                others[len(others)] = discrim_power_table.main_output()
                others_tables[len(others_tables)] = key

        elif ('backtest_pit_PD') in key:
            if '_st' not in key and 'nw' in key:
                print(key)
                PD_DR = GENERAL_BACKTEST_TTC_P1_TABLE(key, 'nw')                                    # TTC calibration by reporting date (portfolio level)
                if key == 'backtest_pit_PD_nw' or '_all' in key or '_oall' in key:                   # NW portfolio level
                    PD_CQ_6[len(PD_CQ_6)] = PD_DR.main_output()
                    PD_CQ_6_tables[len(PD_CQ_6_tables)] = key
                else:                                                                               # NW sub-model level
                    others[len(others)] = PD_DR.main_output()
                    others_tables[len(others_tables)] = key
                try:
                    misestimation_table = 'misestimation_PD' + key.split('backtest_pit_PD')[1]
                except:
                    print('Misestimation table (PD) not found! Check if this is correct, otherwise change the file name!')
                    break
                print(misestimation_table)
                backtest_PD_table = BACKTEST_PIT_TABLE(key, misestimation_table)
                if key == 'backtest_pit_PD_nw' or '_all' in key or '_oall' in key:                   # NW portfolio level
                    PD_CQ_1[len(PD_CQ_1)] = backtest_PD_table.main_output()
                    PD_CQ_1_tables[len(PD_CQ_1_tables)] = key + ' & ' + misestimation_table
                else:                                                                               # NW sub-model level
                    PD_CQ_2[len(PD_CQ_2)] = backtest_PD_table.main_output()
                    PD_CQ_2_tables[len(PD_CQ_2_tables)] = key + ' & ' + misestimation_table
            else:
                for weight in PD_weight:
                    if weight in key:
                        print(key)
                        try:
                            misestimation_table = 'misestimation_PD' + key.split('backtest_pit_PD')[1]
                        except:
                            print('Misestimation table (PD) not found! Check if this is correct, otherwise change the file name!')
                            break
                        print(misestimation_table)
                        backtest_PD_table = BACKTEST_PIT_TABLE(key, misestimation_table)
                        if '_st' and 'nw' in key:                                                   # NW per stage
                            PD_CQ_3[len(PD_CQ_3)] = backtest_PD_table.main_output()
                            PD_CQ_3_tables[len(PD_CQ_3_tables)] = key + ' & ' + misestimation_table
                        elif (key == 'backtest_pit_PD_ew' or key == 'backtest_pit_PD_st1_ew' or key == 'backtest_pit_PD_st2_ew' or '_all' in key or '_oall' in key):    # EW portfolio level (incl. per stage)
                                PD_CQ_4[len(PD_CQ_4)] = backtest_PD_table.main_output()
                                PD_CQ_4_tables[len(PD_CQ_4_tables)] = key + ' & ' + misestimation_table
                        else:                                                                       # EW sub-model level
                            PD_CQ_5[len(PD_CQ_5)] = backtest_PD_table.main_output()
                            PD_CQ_5_tables[len(PD_CQ_5_tables)] = key + ' & ' + misestimation_table
                        break

        elif ('backtest_ttc_PD' in key):
            if key == 'backtest_ttc_PD_rat' or '_rat_all' in key or '_rat_oall' in key:             # portfolio level
                print(key)
                TTC_PD_rating = BACKTEST_TTC_PD_RATING_TABLE(key)
                PD_CQ_6[len(PD_CQ_6)] = TTC_PD_rating.main_output()                                 # TTC backtest rating level
                PD_CQ_6_tables[len(PD_CQ_6_tables)] = key
            elif 'backtest_ttc_PD_rat' in key:                                                      # sub-model level
                print(key)
                TTC_PD_rating_sub = BACKTEST_TTC_PD_RATING_TABLE(key)
                others[len(others)] = TTC_PD_rating_sub.main_output()
                others_tables[len(others_tables)] = key
            elif (key == 'backtest_ttc_PD_nw' or '_all' in key or '_oall' in key) and 'nw' in key:  # portfolio level
                print(key)
                TTC_PD = GENERAL_BACKTEST_TTC_P2_TABLE(key)
                PD_CQ_6[len(PD_CQ_6)] = TTC_PD.main_output()                                        # TTC backtest total level
                PD_CQ_6_tables[len(PD_CQ_6_tables)] = key
            elif 'backtest_ttc_PD_nw' in key:                                                       # sub-model level
                print(key)
                TTC_PD_sub = GENERAL_BACKTEST_TTC_P2_TABLE(key)
                others[len(others)] = TTC_PD_sub.main_output()
                others_tables[len(others_tables)] = key
                
        elif ('misest_ttc_PD_rat' in key):
            if key == 'misest_ttc_PD_rat' or '_all' in key or '_oall' in key:                       # portfolio level
                print(key)
                misest_TTC_PD_rating = MISEST_TTC_PD_RATING_TABLE(key)
                PD_CQ_6[len(PD_CQ_6)] = misest_TTC_PD_rating.main_output()                          # Misestimation TTC rating level
                PD_CQ_6_tables[len(PD_CQ_6_tables)] = key
            else:                                                                                   # sub-model level
                print(key)
                misest_TTC_PD_rating_sub = MISEST_TTC_PD_RATING_TABLE(key)
                others[len(others)] = misest_TTC_PD_rating_sub.main_output()
                others_tables[len(others_tables)] = key

        elif ('ttest2_stage') in key:
            print(key)
            if key == 'ttest2_stage' or '_all' in key or '_oall' in key:                            # portfolio level
                calib_ttest_2sp_stage = CALIB_TTEST_2SP_STAGE_TABLE(key)
                STAGING_CQ_1[len(STAGING_CQ_1)] = calib_ttest_2sp_stage.main_output()
                STAGING_CQ_1_tables[len(STAGING_CQ_1_tables)] = key
            else:                                                                                   # sub-model level
                for segment in sas_output[key]['segment'].unique():
                    calib_ttest_2sp_stage_segm = CALIB_TTEST_2SP_STAGE_TABLE(key, segment)
                    STAGING_CQ_2[len(STAGING_CQ_2)] = calib_ttest_2sp_stage_segm.main_output()
                    STAGING_CQ_2_tables[len(STAGING_CQ_2_tables)] = key + ' (' + segment + ')'

        elif ('ttest1_stage') in key:
            print(key)
            if key == 'ttest1_stage' or '_all' in key or '_oall' in key:                            # portfolio level
                calib_ttest_1sp_stage = CALIB_TTEST_1SP_STAGE_TABLE(key)
                STAGING_CQ_3[len(STAGING_CQ_3)] = calib_ttest_1sp_stage.main_output()
                STAGING_CQ_3_tables[len(STAGING_CQ_3_tables)] = key
            else:                                                                                   # sub-model level
                for segment in sas_output[key]['segment'].unique():
                    calib_ttest_1sp_stage_segm = CALIB_TTEST_1SP_STAGE_TABLE(key, segment)
                    STAGING_CQ_4[len(STAGING_CQ_4)] = calib_ttest_1sp_stage_segm.main_output()
                    STAGING_CQ_4_tables[len(STAGING_CQ_4_tables)] = key + ' (' + segment + ')'

        elif ('backtest_pit_LGD' in key):
            for weight in LGD_weight:
                if weight in key or ('nw' not in key and 'ew' not in key):
                    print(key)
                    try:
                        misestimation_table = 'misestimation_LGD' + key.split('backtest_pit_LGD')[1]
                    except:
                        print('Misestimation table (LGD) not found! Check the file name.')
                        break
                    print(misestimation_table)
                    backtest_LGD_table = BACKTEST_PIT_TABLE(key, misestimation_table)
                    if 'backtest_pit_LGD_st1' in key or 'backtest_pit_LGD_st2' in key:              # EW (performing)
                        if key == 'backtest_pit_LGD_st1_ew' or key == 'backtest_pit_LGD_st2_ew' or key == 'backtest_pit_LGD_st1' or key == 'backtest_pit_LGD_st2' or '_all' in key or '_oall' in key:      # EW portfolio level (performing)
                            LGD_CQ_1[len(LGD_CQ_1)] = backtest_LGD_table.main_output()
                            LGD_CQ_1_tables[len(LGD_CQ_1_tables)] = key + ' & ' + misestimation_table
                        else:                                                                       # EW sub-model level (performing) 
                            LGD_CQ_2[len(LGD_CQ_2)] = backtest_LGD_table.main_output()
                            LGD_CQ_2_tables[len(LGD_CQ_2_tables)] = key + ' & ' + misestimation_table
                    else:                                                                           # EW (in-default)
                        if key == 'backtest_pit_LGD_indef_ew' or key == 'backtest_pit_LGD_indef' or '_all' in key or '_oall' in key:        # EW portfolio level (in-default)
                            LGD_CQ_4[len(LGD_CQ_4)] = backtest_LGD_table.main_output()
                            LGD_CQ_4_tables[len(LGD_CQ_4_tables)] = key + ' & ' + misestimation_table
                        else:                                                                       # EW sub-model level (in-default)
                            LGD_CQ_5[len(LGD_CQ_5)] = backtest_LGD_table.main_output()
                            LGD_CQ_5_tables[len(LGD_CQ_5_tables)] = key + ' & ' + misestimation_table
                    break

        elif ('backtest_ttc_LGD') in key:
            print(key)
            TTC_LGD = GENERAL_BACKTEST_TTC_P2_TABLE(key)
            if key == 'backtest_ttc_LGD_st1' or key == 'backtest_ttc_LGD_st2' or (('_all' in key or '_oall' in key) and '_indef' not in key):     # TTC t-test (performing)
                LGD_CQ_3[len(LGD_CQ_3)] = TTC_LGD.main_output()
                LGD_CQ_3_tables[len(LGD_CQ_3_tables)] = key
            elif (key == 'backtest_ttc_LGD_indef') or ('_all' in key or '_oall' in key):                                                          # TTC t-test (in-default)
                LGD_CQ_6[len(LGD_CQ_6)] = TTC_LGD.main_output()
                LGD_CQ_6_tables[len(LGD_CQ_6_tables)] = key
            else:
                others[len(others)] = TTC_LGD.main_output()
                others_tables[len(others_tables)] = key
        
        elif ('backtest_pit_EAD') in key:
            for weight in EAD_weight:
                if weight in key:
                    print(key)
                    try:
                        misestimation_table = 'misestimation_EAD' + key.split('backtest_pit_EAD')[1]
                    except:
                        misestimation_table = 'misestimation_EAD'
                    if misestimation_table not in sas_output.keys():
                        print('Misestimation table (EAD) not found! Check if this is correct, otherwise change the file name.')
                        break
                    print(misestimation_table)
                    backtest_EAD_table = BACKTEST_PIT_TABLE(key, misestimation_table)
                    if key == 'backtest_pit_EAD_ew' or 'ew_all' in key or 'ew_oall' in key:         # EW portfolio level
                        EAD_CQ_1[len(EAD_CQ_1)] = backtest_EAD_table.main_output()
                        EAD_CQ_1_tables[len(EAD_CQ_1_tables)] = key + ' & ' + misestimation_table
                    else:                                                                           # EW sub-model level
                        EAD_CQ_2[len(EAD_CQ_2)] = backtest_EAD_table.main_output()
                        EAD_CQ_2_tables[len(EAD_CQ_2_tables)] = key + ' & ' + misestimation_table
                    break

        elif ('backtest_pit_ECL') in key:
            for weight in ECL_weight:
                if weight in key or ('nw' not in key and 'ew' not in key):
                    print(key)
                    try:
                        misestimation_table = 'misestimation_ECL' + key.split('backtest_pit_ECL')[1]
                    except:
                        misestimation_table = 'misestimation_ECL'
                    if misestimation_table not in sas_output.keys():
                        print('Misestimation table (ECL) not found! Check if this is correct, otherwise change the file name.')
                        break
                    print(misestimation_table)
                    backtest_ECL_table = BACKTEST_PIT_TABLE(key, misestimation_table)
                    if key == 'backtest_pit_ECL_st1_ew' or key == 'backtest_pit_ECL_st2_ew' or key == 'backtest_pit_ECL_st1' or key == 'backtest_pit_ECL_st2' or '_all' in key or '_oall' in key:      # EW portfolio level
                        ECL_CQ_1[len(ECL_CQ_1)] = backtest_ECL_table.main_output()
                        ECL_CQ_1_tables[len(ECL_CQ_1_tables)] = key + ' & ' + misestimation_table
                    else:                                                                           # EW sub-model level
                        ECL_CQ_2[len(ECL_CQ_2)] = backtest_ECL_table.main_output()
                        ECL_CQ_2_tables[len(ECL_CQ_2_tables)] = key + ' & ' + misestimation_table

                    ECL_DR = GENERAL_BACKTEST_TTC_P1_TABLE(key, weight)
                    ECL_CQ_3[len(ECL_CQ_3)] = ECL_DR.main_output()                                  # TTC calibration by reporting date
                    ECL_CQ_3_tables[len(ECL_CQ_3_tables)] = key
                    break

        elif ('backtest_ttc_ECL') in key:
            for weight in ECL_weight:
                if weight in key or ('nw' not in key and 'ew' not in key):
                    print(key)
                    TTC_ECL = GENERAL_BACKTEST_TTC_P2_TABLE(key)
                    ECL_CQ_3[len(ECL_CQ_3)] = TTC_ECL.main_output()
                    ECL_CQ_3_tables[len(ECL_CQ_3_tables)] = key
                    break

        # other tables (not used in current activities)
        elif ('stability' in key):
            print(key)
            stability_PSI_table = PSI_TABLE(key)
            others[len(others)] = stability_PSI_table.main_output()
            others_tables[len(others_tables)] = key    

        elif ('prov_per_stage' in key):
            print(key)
            provisions_table = PROVISIONS(key)
            others[len(others)] = provisions_table.main_output()
            others_tables[len(others_tables)] = key


    ## Check if all tables have been used to create tables
    all_tables = []
    for test in all_tests:
        for table in globals()[test + '_tables'].values():
            all_tables.append(table.split(' & ')[0])
            all_tables.append(table.split(' (')[0])
            try:
                all_tables.append(table.split(' & ')[1])
            except:
                pass
            try:
                all_tables.append(table.split(' )')[1])
            except:
                pass

    for key in sas_output.keys():
        if key not in all_tables and 'misest_ttc' not in key:
            print(f"{key} has not been used to create tables. Check if this is correct, otherwise change the file name as needed.")

    return


if INCLUDE_TABLES == True:
    generate_tables(sas_output, all_tests)

## Note: The following tables are not used according to the current requirements:
# misest_ttc_ECL_st1
# misest_ttc_ECL_st2
# misest_ttc_LGD_indef
# misest_ttc_LGD_st1
# misest_ttc_LGD_st2
# misest_ttc_PD


#######################################################################################################################
#%%
### Generate the plots
def generate_plots(sas_output, all_tests):
    print("\n\n###################")
    print("Generating plots...")
    print("###################\n")
    for key in sas_output.keys():
        if ('backtest_pit_PD' in key and '_st' not in key):
            for weight in PD_weight:
                if weight in key:
                    print(key)
                    for horizon in PD_horizons:
                        backtest_PD_plot = PD_DR_PLOT(key, weight, horizon)
                        backtest_PD_plot.main_output()
                    break

        elif ('backtest_pit_PD' in key and '_st' in key):
            for weight in PD_weight:
                if weight in key:
                    for stage in PD_stages:
                        if '_st' + str(stage) in key:
                            print(key)
                            for horizon in PD_horizons:
                                backtest_PD_plot = GENERAL_TS_PLOT(key, weight, stage, horizon)
                                backtest_PD_plot.main_output()
                            break

        elif ('backtest_pit_EAD' in key):
            for weight in EAD_weight:
                if weight in key:
                    print(key)
                    for horizon in EAD_horizons:
                        backtest_EAD_plot = EAD_PLOT(key, weight, horizon)
                        backtest_EAD_plot.main_output()
                    break

        elif ('stability' in key):
            for weight in PSI_weight:
                if weight in key.lower():
                    print(key)
                    stability_PSI_plot = PSI_PLOT(key, weight)
                    stability_PSI_plot.main_output()
                    break

        elif ('discrim_power_stage' in key):
            print(key)
            for horizon in STAGING_horizons:
                discrim_power_stage_plot = DISCRIM_POWER_STAGE_PLOT(key, horizon)
                discrim_power_stage_plot.main_output()

        elif ('backtest_pit_LGD' in key):
            for weight in LGD_weight:
                if weight in key or ('nw' not in key and 'ew' not in key):
                    for stage in LGD_stages:
                        if '_st' + str(stage) in key or f'_{str(stage)}' in key:
                            print(key)
                            for horizon in LGD_horizons:
                                backtest_LGD_plot = GENERAL_TS_PLOT(key, weight, stage, horizon)
                                backtest_LGD_plot.main_output()
                            break
                    break

        elif ('BACKTEST_PIT_CURE' in key.upper() or 'BACKTEST_PIT_NOLOSS' in key.upper()):
            for weight in cure_weight:
                if weight in key.lower():
                    print(key)
                    cure_plot = CURE_PLOT(key, weight = 'nw', method = 'pit')
                    cure_plot.main_output()
                    break

        elif ('backtest_pit_ECL' in key):
            for weight in ECL_weight:
                if weight in key or ('nw' not in key and 'ew' not in key):
                    for stage in ECL_stages:
                        if '_st' + str(stage) in key:
                            print(key)
                            for horizon in ECL_horizons:
                                backtest_ECL_plot = GENERAL_TS_PLOT(key, weight, stage, horizon)
                                backtest_ECL_plot.main_output()
                            break


    ## Check if all tables have been used to create tables
    all_plots = []
    for test in all_tests:
        for plot in globals()[test + '_plots'].values():
            all_plots.append(plot.split(' & ')[0])
            all_plots.append(plot.split(' (')[0])
            try:
                all_plots.append(plot.split(' & ')[1])
            except:
                pass
            try:
                all_plots.append(plot.split(' )')[1])
            except:
                pass

    for key in sas_output.keys():
        if key not in all_plots and ('misest' not in key and 'ttc' not in key and 'ttest' not in key and 'prov_per_stage' not in key):
            try:
                key.split('discrim_power_')[1]
            except:
                continue
            else:
                if 'stage' in key.split('discrim_power_')[1]:
                    print(f"{key} has not been used to create plots. Check if this is correct, otherwise change the file name as needed.")

    return

if INCLUDE_PLOTS == True:
    generate_plots(sas_output, all_tests)


#######################################################################################################################
#%%
### Excel generator
# create dictionary with all the results
results_dict = {}
for test in all_tests:
    results_dict[test] = {}
    try:
        results_dict[test] = eval(test)
    except:
        results_dict[test] = pd.DataFrame()
    try:
        results_dict[test]['Tables'] = eval(test + '_tables')
    except:
        results_dict[test]['Tables'] = []
    try:
        results_dict[test]['Plots'] = eval(test + '_plots')
    except:
        results_dict[test]['Plots'] = []


## function to generate Excel file with all the output tables/plots
def generate_excel(results_dict, filename):
    print("\n\n########################")
    print("Generating Excel file...")
    print("########################\n")
    try:
        writer = pd.ExcelWriter(f"{newfolder}/{filename}", engine = 'xlsxwriter')
    except:
        print('ERROR: Excel file could not be generated. Please check the path and filename, or make sure to close the current Excel file!')
        return
    workbook = writer.book

    activity_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 9, 'valign': 'vcenter', 
                                           'align': 'left', 'bold': True})
    description_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 9, 'valign': 'vcenter', 
                                              'align': 'left'})
    text_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'num_format': '0.00%', 
                                    'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': 'black'})


    # standard starting row
    start_row = 6

    ## Table formatting function
    def format_table(df, worksheet, start_row):
        header_format = workbook.add_format({'bg_color':'#ff6200', 'font_name': 'ING Me', 'font_color': '#ffffff', 'text_wrap': True, 'font_size': 8,
                                         'align': 'center', 'valign': 'vcenter', 'bold': True, 'border': 1, 'border_color': 'black'})
        input_format = workbook.add_format({'italic': True, 'font_name': 'ING Me', 'font_size': 8})
        bold_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'num_format': '0.00%', 'bold': True,
                                           'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': 'black'})
        conclusion_red_format = workbook.add_format({'bold': True, 'font_color': '#9C0006', 'bg_color': '#FEB0A8'})
        conclusion_yellow_format = workbook.add_format({'bold': True, 'font_color': '#CC9900', 'bg_color': '#FFFF97'})
        conclusion_green_format = workbook.add_format({'bold': True, 'font_color': '#006100', 'bg_color': '#ddf7bb'})
        # first_column_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'num_format': '0', 
        #                                    'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': 'black'})
        integer_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'num_format': '#,##0', 
                                           'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': 'black'})
        score_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'num_format': '0.00', 
                                           'valign': 'vcenter', 'align': 'center', 'border': 1, 'border_color': 'black'})
        to_be_filled_format = workbook.add_format({'font_name': 'ING Me', 'font_size': 8, 'valign': 'vcenter', 
                                           'align': 'center', 'border': 1, 'border_color': 'black', 'bg_color': 'yellow'})
        empty_format = workbook.add_format({'pattern': 14})

        # have a space of 1 white column between tables
        start_col = {}
        init_col = 1
        for i in range(len(df.keys()) - 1):
            if i == 0:
                start_col[i] = init_col
            else:
                start_col[i] = start_col[i-1] + len(df[list(df.keys())[i-1]].columns) + 1

        # activity description
        worksheet.set_column_pixels(0, 0, 100)
        worksheet.write('A1', 'Activity:', activity_format)
        worksheet.write('A2', 'Level:', activity_format)
        worksheet.write('A3', 'SAS tables:', activity_format)
        if 'Tables' in df.keys():
            worksheet.write('B3', ', '.join(f'{value}' for key, value in df['Tables'].items()), description_format)

        worksheet.write('A4', 'Comments:', activity_format)

        # format table
        for key in df.keys():
            if key in ['Tables', 'Plots']:
                continue
            for col_num, col_data in enumerate(df[key].T.reset_index().values.tolist()):
                if 'RATING' in col_data[0].upper() or 'POOL' in col_data[0].upper():
                    worksheet.write_column(start_row, start_col[key] + col_num, col_data, integer_format)
                elif 'SCORE' in col_data[0].upper() or 'STATISTIC' in col_data[0].upper() or 'VALUE' in col_data[0].upper():
                    worksheet.write_column(start_row, start_col[key] + col_num, col_data, score_format)
                else:
                    worksheet.write_column(start_row, start_col[key] + col_num, col_data, text_format)

        # format headers
        for key in df.keys():
            if key in ['Tables', 'Plots']:
                continue
            for col_num, value in enumerate(df[key].columns.values):
                worksheet.write(start_row, start_col[key] + col_num, value, header_format)
                worksheet.set_column(start_col[key] + col_num, start_col[key] + col_num, min(22, len(value) + 2))    # set column width based on headers
            worksheet.write(start_row - 1, start_col[key], df['Tables'][key], input_format)

        # format special rows (i.e. Overall)
        for key in df.keys():
            if key in ['Tables', 'Plots']:
                continue
            for row_num, value in enumerate(df[key].values.tolist()):
                if value[0] in ['Overall']:
                    worksheet.write_row(start_row + 1 + row_num, start_col[key], value, bold_format)

        # N/A
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"  "',
                                    'format': empty_format})
        
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"."',
                                    'format': empty_format})
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"XXX"',
                                    'format': to_be_filled_format})

        # conclusion colours
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"Fail"',
                                    'format': conclusion_red_format})
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"Red"',
                                    'format': conclusion_red_format})
        
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"Yellow"',
                                    'format':  conclusion_yellow_format})
        
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"Pass"',
                                    'format': conclusion_green_format})
        worksheet.conditional_format('A2:ZZ999', {'type': 'cell',
                                    'criteria': '==',
                                    'value': '"Green"',
                                    'format': conclusion_green_format})
        

        # # set column width and format of other cells
        # worksheet.set_column(0, 99, 11, others_format)

        return
    
    ## Function to create a worksheet, populate with the worksheet with tables/plots and format the tables
    def create_worksheet(sheet_name, model, table_string, activity_num, activity_descr, level):
        worksheet = workbook.add_worksheet(sheet_name)
        plots_exist = False

        # activity description
        worksheet.write('B1', activity_num, activity_format)
        worksheet.write('C1', activity_descr, description_format)
        worksheet.write('B2', level, description_format)
        try:
            if (not results_dict[table_string]['Tables'] and not [file for file in os.listdir(f"{newfolder}/plots/{model}/") if table_string in file]):
                worksheet.write('B4', 'No data available', description_format)
        except:
            if (not results_dict[table_string]['Tables']):
                worksheet.write('B4', 'No data available', description_format)
        
        # insert tables
        format_table(results_dict[table_string], worksheet, start_row)

        # insert plots
        if ([file for file in os.listdir(f"{newfolder}/plots/{model}/") if table_string in file] or table_string == 'others'):
            plots_exist = True
            worksheet.write('B4', f"[Tables only, for plots go to sheet {sheet_name} - Plots]", description_format)

            worksheet_2 = workbook.add_worksheet(sheet_name + ' - Plots')
            hspace = start_row
            for file in os.listdir(f"{newfolder}/plots/{model}/"):
                if (table_string in file and file.endswith('.png') or table_string == 'others'):
                    worksheet_2.insert_image('B' + str(hspace), f"{newfolder}/plots/{model}/{file}", {'x_scale': 0.55, 'y_scale': 0.6})
                    hspace += 15

            # activity description
            format_table(pd.DataFrame(), worksheet_2, start_row)
            worksheet_2.write('B1', activity_num, activity_format)
            worksheet_2.write('C1', activity_descr, description_format)
            worksheet_2.write('B2', level, description_format)
            worksheet_2.write('B3', ', '.join(f'{value}' for key, value in results_dict[table_string]['Plots'].items()), description_format)
            worksheet_2.write('B4', '[Plots only]', description_format)

        if plots_exist == True:
            return worksheet, worksheet_2
        else:
            return worksheet

    ## PD Model Output - Calibration Quality (3.7.2.1)
    def output_PD_CQ():
        ## 1 - NW PiT CQ (portfolio level)
        create_worksheet("PD CQ #1", 'PD', 'PD_CQ_1',
                         '3.7.2.1.1', "Assess the multi-year number-weighted PiT calibration quality of the overall PD model at portfolio level.",
                         'Portfolio level')

        ## 2 - NW PiT CQ (sub-model level)
        create_worksheet("PD CQ #2", 'PD', 'PD_CQ_2',
                         '3.7.2.1.2', "Assess the multi-year number-weighted PiT calibration quality of the overall PD model at sub-model level where applicable.",
                         'Sub-model level')

        ## 3 - NW PiT CQ (per Stage)
        create_worksheet("PD CQ #3", 'PD', 'PD_CQ_3',
                         '3.7.2.1.3', "Assess the multi-year number-weighted PiT calibration quality of the overall PD model per Stage.",
                         'Stage level')

        ## 4 - EW PiT CQ (portfolio level)
        create_worksheet("PD CQ #4", 'PD', 'PD_CQ_4',
                         '3.7.2.1.4', "Assess the multi-year exposure-weighted PiT calibration quality of the overall PD model at portfolio level.",
                         'Portfolio level')

        ## 5 - NW PiT CQ (per Stage)
        create_worksheet("PD CQ #5", 'PD', 'PD_CQ_5',
                         '3.7.2.1.5', "Assess the multi-year exposure-weighted PiT calibration quality of the overall PD model at sub-model level (where applicable).",
                         'Sub-model level')

        ## 6 - NW PiT CQ (per Stage)
        create_worksheet("PD CQ #6", 'PD', 'PD_CQ_6',
                         '3.7.2.1.6', "Assess the 12-month number-weighted long-run average calibration quality of the overall PD model at portfolio level using t-test for comparing the average PD to the average observed default rate (p-value of the t-test to be computed).",
                         'Portfolio level')
        
        return

    ## Staging Model Output - Discrimination Power (3.7.2.2)
    def output_STAGING_DP():
        ## 1 - MCC & Type II error (portfolio level)
        create_worksheet("Staging DP #1", 'Staging', 'STAGING_DP_1',
                         '3.7.2.2.1', "Compute the Mathews Correlation Coefficient and Type II error over time of the staging model at portfolio level.",
                         'Portfolio level')
        
        ## 2 - MCC & Type II error (sub-model level)
        create_worksheet("Staging DP #2", 'Staging', 'STAGING_DP_2',
                         '3.7.2.2.2', "Compute the Mathews Correlation Coefficient and Type II error over time of the staging model at segment level, where applicable.",
                         'Sub-model level')
        
        ## 3 - MCC development vs most recent snapshot (portfolio level)
        STAGING_DP_3_sheet = create_worksheet("Staging DP #3", 'Staging', 'STAGING_DP_3',
                         '3.7.2.2.3', "Compute the change in the Mathews Correlation Coefficient of the most recent snapshot (with a 12 month performance window) compared to the development sample at overall staging model at portfolio level.",
                         'Portfolio level')
        if (not results_dict['STAGING_DP_3']['Tables']):
            STAGING_DP_3_sheet.write('B4', 'No data available', description_format)
        else:
            STAGING_DP_3_sheet.write('B4', '[Manually fill in MCC (development) as this is not computed in SAS. Relative & absolute change will be updated automatically]', description_format)
            STAGING_DP_3_sheet.write_formula(f'D{start_row + 2}', f'=(C{start_row + 2}-B{start_row + 2})/B{start_row + 2}', text_format)
            STAGING_DP_3_sheet.write_formula(f'E{start_row + 2}', f'=ABS(B{start_row + 2}-C{start_row + 2})', text_format)

        return

    ## Staging Model Output - Calibration Quality (3.7.2.3)
    def output_STAGING_CQ():
        ## 1 - NW two-sample T-test (portfolio level)
        create_worksheet("Staging CQ #1", 'Staging', 'STAGING_CQ_1',
                         '3.7.2.3.1', "Assess whether the number-weighted cumulative stage 1 and 2 observed default rates at portfolio level are significantly different (two-sample one-sided t-test) (p-value of the t-test to be computed).",
                         'Portfolio level')
        
        ## 2 - NW two-sample T-test (sub-model level)
        create_worksheet("Staging CQ #2", 'Staging', 'STAGING_CQ_2',
                         '3.7.2.3.2', "Assess whether the number-weighted cumulative stage 1 and 2 observed default rates at sub-model level are significantly different (two-sample one-sided t-test) (p-value of the t-test to be computed).",
                         'Sub-model level')
        
        ## 3 - NW one-sample T-test (portfolio level)
        create_worksheet("Staging CQ #3", 'Staging', 'STAGING_CQ_3',
                         '3.7.2.3.3', "Assess whether the number-weighted cumulative stage 2 observed default rate and the conditional PD at origination at portfolio level are significantly different (two-sample one-sided t-test, p-value of the t-test to be computed).",
                         'Portfolio level')
        
        ## 4 - NW one-sample T-test (sub-model level)
        create_worksheet("Staging CQ #4", 'Staging', 'STAGING_CQ_4',
                         '3.7.2.3.4', "Assess whether the number-weighted cumulative stage 2 observed default rate and the conditional PD at origination at sub-model level are significantly different (two-sample one-sided t-test, p-value of the t-test to be computed).",
                         'Sub-model level')
        
        return
        
    ## LGD Model Output - Calibration Quality (3.8.2.1)
    def output_LGD_CQ():
        ## 1 - EW PiT CQ (portfolio level) - performing
        create_worksheet("LGD CQ #1", 'LGD', 'LGD_CQ_1',
                         '3.8.2.1.1', "Assess the multi-year exposure-weighted PiT calibration quality of the performing LGD model at portfolio level.",
                         'Portfolio level')
        
        ## 2 - EW PiT CQ (sub-model level) - performing
        create_worksheet("LGD CQ #2", 'LGD', 'LGD_CQ_2',
                         '3.8.2.1.2', "Assess the multi-year exposure-weighted PiT calibration quality of the performing LGD model at sub-model level where applicable.",
                         'Sub-model level')
        
        ## 3 - 12-month LRA CQ (portfolio level) - performing
        create_worksheet("LGD CQ #3", 'LGD', 'LGD_CQ_3',
                         '3.8.2.1.3', "Assess the 12 month exposure-weighted long-run average calibration quality of the performing LGD model at portfolio level where applicable using t-test (p-value to be computed).",
                         'Portfolio level')
        
        ## 4 - EW PiT CQ (portfolio level) - in-default
        create_worksheet("LGD CQ #4", 'LGD', 'LGD_CQ_4',
                         '3.8.2.1.4', "Assess the exposure-weighted PiT calibration quality of the In-Default LGD model at portfolio level, where applicable.",
                         'Portfolio level')
        
        ## 5 - EW PiT CQ (sub-model level) - in-default
        create_worksheet("LGD CQ #5", 'LGD', 'LGD_CQ_5',
                         '3.8.2.1.5', "Assess the exposure-weighted PiT calibration quality of the In-Default LGD model at sub-model level, where applicable.",
                         'Sub-model level')
        
        ## 6 - LRA CQ (portfolio level) - in-default
        create_worksheet("LGD CQ #6", 'LGD', 'LGD_CQ_6',
                         '3.8.2.1.6', "Assess the exposure-weighted long-run average calibration quality of the In-Default LGD model at portfolio level, where applicable using t-test (p-value to be computed).",
                         'Portfolio level')
        
        return

    ## EAD Model Output - Calibration Quality (3.9.2.1)
    def output_EAD_CQ():
        ## 1 - EW PiT CQ (portfolio level)
        create_worksheet("EAD CQ #1", 'EAD', 'EAD_CQ_1',
                         '3.9.2.1.1', "Assess the multi-year exposure-weighted PiT calibration quality of the EAD model at portfolio level where applicable. Compute and plot the EAD exposure-weighted accuracy ratio (observed divided by predicted) over time and compare to 100%.",
                         'Portfolio level')
        
        ## 2 - EW PiT CQ (product level)
        create_worksheet("EAD CQ #2", 'EAD', 'EAD_CQ_2',
                         '3.9.2.1.2', "Assess the multi-year exposure-weighted PiT calibration quality of the EAD model at product level where applicable. Compute and plot the EAD exposure-weighted accuracy ratio (observed divided by predicted) over time and compare to 100%.",
                         'Product level')
        
        return

    ## ECL Model Output - Calibration Quality (3.10.1.1)
    def output_ECL_CQ():
        ## 1 - EW PiT CQ (portfolio level)
        create_worksheet("ECL CQ #1", 'ECL', 'ECL_CQ_1',
                         '3.10.1.1.1', "Assess the multi-year exposure-weighted PiT calibration quality for the Stage 1 and 2 ECL at portfolio level where applicable based on a normal distribution of portfolio Stage 1 and 2 ECL.",
                         'Portfolio level')
        
        ## 2 - EW PiT CQ (sub-model level)
        create_worksheet("ECL CQ #2", 'ECL', 'ECL_CQ_2',
                         '3.10.1.1.2', "Assess the multi-year exposure-weighted PiT calibration quality for the Stage 1 and 2 ECL at sub-model level where applicable based on a normal distribution of portfolio Stage 1 and 2 ECL.",
                         'Sub-model level')
        
        ## 3 - 12-month EW LRA CQ T-test (portfolio level)
        create_worksheet("ECL CQ #3", 'ECL', 'ECL_CQ_3',
                         '3.10.1.1.3', "Assess the 12 month exposure-weighted long-run average calibration quality of the Stage 1 and 2 ECL model at portfolio level where applicable using a t-test for comparing the average predicted loss rate to the average observed loss rate (p-value of the t-test to be computed).",
                         'Portfolio level')
        
        return
    
    ## Others - Tables that have been created but are not part of the current activities
    def output_others():
        create_worksheet("Others", 'Others', 'others',
                         "These tables/plots are no longer part of a certain activity, but are available here if needed.", "",
                         '')


    ## Generate the sheets per parameter (adjust INCLUDE_... in the parameters.py file)
    if INCLUDE_PD == True:
        output_PD_CQ()
    if INCLUDE_STAGING == True:
        output_STAGING_DP()
        output_STAGING_CQ()
    if INCLUDE_LGD == True:
        output_LGD_CQ()
    if INCLUDE_EAD == True:
        output_EAD_CQ()
    if INCLUDE_ECL == True:
        output_ECL_CQ()
    if INCLUDE_OTHERS == True:
        output_others()


    ## Set tab/sheet colours
    for sheet in writer.sheets:
        if 'PD CQ' in sheet:
            writer.sheets[sheet].set_tab_color('#203764')
        elif 'Staging DP' in sheet:
            writer.sheets[sheet].set_tab_color('#538DD5')
        elif 'Staging CQ' in sheet:
            writer.sheets[sheet].set_tab_color('#8DB4E2')
        elif 'LGD CQ' in sheet:
            writer.sheets[sheet].set_tab_color('#963634')
        elif 'EAD CQ' in sheet:
            writer.sheets[sheet].set_tab_color('#C4D79B')
        elif 'ECL CQ' in sheet:
            writer.sheets[sheet].set_tab_color('#E26B0A')
        elif 'Others' in sheet:
            writer.sheets[sheet].set_tab_color('#BFBFBF')


    writer.close()
    print(f"Excel file generated under the name: {filename} in the folder '{newfolder}' in the root directory.\n\n")
    os.startfile(path + '/' + newfolder + '/' + filename)

    return


# create Excel file containing all results
generate_excel(results_dict, filename = output_filename)


