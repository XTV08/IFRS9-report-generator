###################################################################################
######################## [TECHNICAL CODE] (DO NOT CHANGE) #########################
###################################################################################

###################################################################################
##################################### CLASSES #####################################
###################################################################################


## import libraries
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import re

# import data from other python files
from parameters import *                # import parameters from the parameters.py file in the root folder

###################################################################################

## Initialise dictionary to store the input tables
all_tests = ['PD_CQ_1', 'PD_CQ_2', 'PD_CQ_3', 'PD_CQ_4', 'PD_CQ_5', 'PD_CQ_6',
             'STAGING_DP_1', 'STAGING_DP_2', 'STAGING_DP_3', 'STAGING_CQ_1', 'STAGING_CQ_2', 'STAGING_CQ_3', 'STAGING_CQ_4',
             'LGD_CQ_1', 'LGD_CQ_2', 'LGD_CQ_3', 'LGD_CQ_4', 'LGD_CQ_5', 'LGD_CQ_6',
             'EAD_CQ_1', 'EAD_CQ_2', 'ECL_CQ_1', 'ECL_CQ_2', 'ECL_CQ_3',
             'others']

for test in all_tests:
    vars()[test + '_plots'] = {}
    

###################################################################################
###################################################################################

### PLOTS

# PD backtest plot: PD vs. Observed DR over time for the first horizon
class PD_DR_PLOT:
    def __init__(self, table_name, weight, horizon):
        self.type = 'plot'
        self.table_name = table_name
        self.UB_PD = 'UB_PD'
        self.LB_PD = 'LB_PD'
        self.odr = 'odr'
        self.pit_prediction = 'pit_prediction'
        self.horizon = horizon
        self.weight = weight
        self.dataset = sas_output[table_name]
        self.data = self.dataset.loc[self.dataset.horizon == self.horizon]
        try:
            self.sublevel = self.table_name.split(weight + '_')[1].lower()
            if self.sublevel in ['all', 'oall']:
                self.sublevel = None
        except:
            self.sublevel = None

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]

        weight = self.weight  # nw/ew
        if self.horizon == 0:
            order = 'first'
        elif self.horizon == 1:
            order = 'second'
        elif self.horizon == 2:
            order = 'third'
        elif self.horizon == 3:
            order = 'fourth'
        elif self.horizon == 4:
            order = 'fifth'

        x = np.arange(0, len(self.data.iloc[:, 0]))
        y = self.data[f'{weight}_{self.pit_prediction}'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        y_2 = self.data[f'{weight}_{self.odr}'].apply(lambda x: re.sub('[( %)]', '', x)).astype('float') / 100.0
        try:
            y_ub = self.data[self.UB_PD].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data[self.LB_PD].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        except:
            y_ub = self.data['UB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data['LB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        # ticks = self.data['reporting_date']
        ticks = self.data.iloc[:, 0]  # refer to column 'reporting_date' by index
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # Create the line plot for series Estimated PD
        plt.plot(x, y, ls='-', lw=2.5, color='orangered', alpha=0.7, label='Estimated PD')
        # Create shadow indicating CI
        plt.fill_between(x, y_lb, y_ub, color='mistyrose', alpha=0.5)
        # Add the line plot for series observed Default Rate (DR)
        plt.plot(x, y_2, ls='-', lw=2.5, color='grey', alpha=0.8, label='Observed DR')

        # Setting correct ticks for x axis
        # Rotation is necessary, without it the longer ticks get cut
        plt.xticks(x[::freq], ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        plt.ylabel('Estimated PD & Observed DR', fontsize=12)
        # Add legend
        plt.legend(loc='best', frameon=False)
        # Add horizontal lines
        plt.grid(axis='y', ls=':', lw=0.3)
        # Add title for the figure
        if self.sublevel == None or sublevel_in_title == False:
            plt.title(f'PiT PD Backtest for the {order} year horizon ({weight.upper()})')
        else:
            plt.title(f'PiT PD Backtest for the {order} year horizon ({weight.upper()}) - {self.sublevel.replace("_", " ").title()}')

        # Show and save the plot
        if weight == 'nw' and self.sublevel == None:
            plt.savefig(newfolder + '/plots/PD/' + 'PD_CQ_1_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            PD_CQ_1_plots[len(PD_CQ_1_plots)] = self.table_name
        elif weight == 'nw' and self.sublevel != None:
            plt.savefig(newfolder + '/plots/PD/' + 'PD_CQ_2_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            PD_CQ_2_plots[len(PD_CQ_2_plots)] = self.table_name
        elif weight == 'ew' and self.sublevel == None:
            plt.savefig(newfolder + '/plots/PD/' + 'PD_CQ_4_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            PD_CQ_4_plots[len(PD_CQ_4_plots)] = self.table_name
        elif weight == 'ew' and self.sublevel != None:
            plt.savefig(newfolder + '/plots/PD/' + 'PD_CQ_5_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            PD_CQ_5_plots[len(PD_CQ_5_plots)] = self.table_name
        else:
            print("PD_DR_PLOT not saved, error in file name!")
        if show_plots == True:
            plt.show()
        plt.close()

# PiT Backtest ECL/LGD/PD (stage 1/2/3)
class GENERAL_TS_PLOT:
    def __init__(self, table_name, weight, stage, horizon):
        self.type = 'plot'
        self.table_name = table_name
        self.dataset = sas_output[table_name]
        self.col_horizon = 'horizon'
        self.horizon = horizon
        self.weight = weight
        if stage == 'indef':
            self.stage = 3
        else:
            self.stage = stage
        self.data = self.dataset.loc[self.dataset[self.col_horizon] == self.horizon]
        try:
            if f'_{weight}' not in table_name:
                if stage in [1, 2]:
                    self.sublevel = table_name.split('_st' + str(stage) + '_')[1].lower()
                else:
                    self.sublevel = table_name.split('_indef_')[1].lower()
                if self.sublevel in ['all', 'oall']:
                    self.sublevel = None
            else:
                self.sublevel = self.table_name.split(weight + '_')[1].lower()
                if self.sublevel in ['all', 'oall']:
                    self.sublevel = None
        except:
            self.sublevel = None

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]
        plt.rcParams['xtick.major.pad'] = 8

        weight = self.weight  # nw/ew
        # seg = re.sub('[^A-Z]', '', self.table_name)  # PD/LGD/ECL
        if '_PD_' in self.table_name:
            stage = self.stage  # 1/2 for PD only
        elif ('_LGD_' in self.table_name and 'indef' in self.table_name) or ('_LGD_' in self.table_name and self.stage == 3):
            stage = '3'
            indef_ = 'in-default'  # for in-default LGD only
        elif '_LGD_' in self.table_name and 'indef' not in self.table_name:
            stage = self.stage  # 1/2 for LGD also (based on the updated LGD SAS scripts)
            indef_ = 'performing'
        elif '_ECL_' in self.table_name:
            stage = self.stage  # 1/2 for ECL only
        if self.horizon == 0:
            order = 'first'
        elif self.horizon == 1:
            order = 'second'
        elif self.horizon == 2:
            order = 'third'
        elif self.horizon == 3:
            order = 'fourth'
        elif self.horizon == 4:
            order = 'fifth'

        # Define variables indicating predicted/observed values and set up labels
        if '_LGD_' in self.table_name:
            pred_var = f'LGD_pred_EW'
            obs_var = f'LGD_obs_EW'
            label_ = 'LGD'
            seg = 'LGD'
        elif '_ECL_' in self.table_name:
            pred_var = 'ELR_mar'
            obs_var = 'OLR_mar'
            label_ = 'LR'
            seg = 'ECL'
        elif '_PD_' in self.table_name:
            pred_var = f'{weight}_pit_prediction'
            obs_var = f'{weight}_odr'
            label_ = 'PD'
            seg = 'PD'

        x = np.arange(0, len(self.data.iloc[:, 0]))
        y = self.data[pred_var].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        y_2 = self.data[obs_var].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        try:
            y_ub = self.data[f'UB_{seg}'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data[f'LB_{seg}'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        except:
            y_ub = self.data['UB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data['LB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        # ticks = self.data['reporting_date']
        ticks = self.data.iloc[:, 0]  # refer to column 'reporting_date' by index
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # Create the line plot for series Estimated value
        plt.plot(x, y, ls=':', lw=1.5, color='tomato', marker='D', ms=4, mfc='tomato', alpha=0.7,
                 label=f'Estimated {label_}')
        # Create shadow indicating CI
        plt.fill_between(x, y_lb, y_ub, color='mistyrose', alpha=0.5)
        # Add the line plot for series observed value
        if seg != 'PD':
            plt.plot(x, y_2, ls=':', lw=1.5, color='darkgrey', marker='D', ms=4, mfc='darkgrey', alpha=0.9,
                     label=f'Observed {label_}')
        else:
            plt.plot(x, y_2, ls=':', lw=1.5, color='darkgrey', marker='D', ms=4, mfc='darkgrey', alpha=0.9,
                     label='Observed DR')
        # Setting correct ticks for x axis
        # Rotation applies when more than 5 data points to be displayed
        if len(self.data) in range(1, 8):
            plt.xticks(x[::freq], ticks[::freq], rotation=0, ha='center')
        else:
            plt.xticks(x[::freq], ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        if seg != 'PD':
            plt.ylabel(f'Estimated & Observed {label_}', fontsize=12)
        else:
            plt.ylabel(f'Estimated PD & Observed DR', fontsize=12)
        # Add legend
        plt.legend(loc='best', frameon=False)
        # Add horizontal lines
        plt.grid(axis='y', ls=':', lw=0.3)
        # Add title for the figure
        if self.sublevel == None or sublevel_in_title == False:
            plt.title(f'PiT {seg} Backtest for the {order} year horizon ({weight.upper()} - Stage {stage})')
        else:
            plt.title(f'PiT {seg} Backtest for the {order} year horizon ({weight.upper()} - Stage {stage}) - {self.sublevel.replace("_", " ").title()}')

        # Show and save the plot
        if seg == 'PD' and weight == 'nw':
            if self.sublevel == None:
                plt.savefig(newfolder + '/plots/PD/PD_CQ_3_st' + str(stage) + '_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            else:
                plt.savefig(newfolder + '/plots/PD/PD_CQ_3_st' + str(stage) + '_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            PD_CQ_3_plots[len(PD_CQ_3_plots)] = self.table_name
        elif seg == 'LGD' and indef_ == 'performing' and self.sublevel == None:
            plt.savefig(newfolder + '/plots/LGD/LGD_CQ_1_st' + str(stage) + '_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            LGD_CQ_1_plots[len(LGD_CQ_1_plots)] = self.table_name
        elif seg == 'LGD' and indef_ == 'performing' and self.sublevel != None:
            plt.savefig(newfolder + '/plots/LGD/LGD_CQ_2_st' + str(stage) + '_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            LGD_CQ_2_plots[len(LGD_CQ_2_plots)] = self.table_name
        elif seg == 'LGD' and indef_ == 'in-default' and self.sublevel == None:
            plt.savefig(newfolder + '/plots/LGD/LGD_CQ_4_st' + str(stage) + '_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            LGD_CQ_4_plots[len(LGD_CQ_4_plots)] = self.table_name
        elif seg == 'LGD' and indef_ == 'in-default' and self.sublevel != None:
            plt.savefig(newfolder + '/plots/LGD/LGD_CQ_5_st' + str(stage) + '_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            LGD_CQ_5_plots[len(LGD_CQ_5_plots)] = self.table_name
        elif seg == 'ECL' and self.sublevel == None:
            plt.savefig(newfolder + '/plots/ECL/ECL_CQ_1_st' + str(stage) + '_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            ECL_CQ_1_plots[len(ECL_CQ_1_plots)] = self.table_name
        elif seg == 'ECL' and self.sublevel != None:
            plt.savefig(newfolder + '/plots/ECL/ECL_CQ_2_st' + str(stage) + '_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            ECL_CQ_2_plots[len(ECL_CQ_2_plots)] = self.table_name
        else:
            plt.savefig(newfolder + '/plots/Others/' + 'GENERAL_TS_PLOT_' + seg + '_st' + str(stage) + '_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            others_plots[len(others_plots)] = self.table_name
            print("GENERAL_TS_PLOT not saved as a specific activity! Saved in the 'others' folder.\nCheck if this is correct! (i.e. backtest PD EW for stages are not included in a specfic activity)\n")
        if show_plots == True:
            plt.show()
        plt.close()

# EAD backtest plot: EAD ratio over time (exposure-weighted) for the first horizon
class EAD_PLOT:
    def __init__(self, table_name, weight, horizon):
        # table_name should be the CSV file name (excluding .csv) of the table used for the plot
        # weight should be 'ew' or 'nw'
        self.type = 'plot'
        self.table_name = table_name
        self.dataset = sas_output[table_name]
        self.weight = weight
        self.col_horizon = 'horizon'
        self.horizon = horizon
        self.EAD_ratio_avg = 'EAD_ratio_avg_EW'
        self.y_ub = 'UB_EAD'
        self.y_lb = 'LB_EAD'
        try:
            self.sublevel = self.table_name.split(weight + '_')[1].lower()
            if self.sublevel in ['all', 'oall']:
                self.sublevel = None
        except:
            self.sublevel = None

        self.data = self.dataset.loc[self.dataset[self.col_horizon] == self.horizon]

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]
        plt.rcParams['xtick.major.pad'] = 8

        weight = self.weight  # nw/ew
        if self.horizon == 0:
            order = 'first'
        elif self.horizon == 1:
            order = 'second'
        elif self.horizon == 2:
            order = 'third'
        elif self.horizon == 3:
            order = 'fourth'
        elif self.horizon == 4:
            order = 'fifth'

        x = np.arange(0, len(self.data.iloc[:, 0]))
        y = self.data[self.EAD_ratio_avg].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        try:
            y_ub = self.data[self.y_ub].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data[self.y_lb].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        except:
            y_ub = self.data['UB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data['LB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        # ticks = self.data['reporting_date']
        ticks = self.data.iloc[:, 0]  # refer to column 'reporting_date' by index
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # Create the line plot for series PSI
        plt.fill_between(x, y, 1, where=(y <= y_ub) & (y >= y_lb), facecolor='green', alpha=0.2, interpolate=True)
        plt.fill_between(x, y, 1, where=(y > y_ub) | (y < y_lb), facecolor='red', alpha=0.2, interpolate=True)
        plt.vlines(x, ymin=1, ymax=y, color='grey', alpha=0.7, lw=1, ls='--')
        plt.plot(x, y, ls='', lw=2, color='grey', marker='D', ms=7, mfc='grey', alpha=0.8, label='Observed EAD ratio')
        plt.plot(x, y_lb, ls='--', lw=1.5, color='slategray', marker='', ms=8, mfc='pink', alpha=0.5, label='CI')
        plt.plot(x, y_ub, ls='--', lw=1.5, color='slategray', marker='', ms=8, mfc='pink', alpha=0.5)

        # Setting correct ticks for x axis
        # Rotation applies when more than 5 data points to be displayed
        if len(self.data) in range(1, 6):
            plt.xticks(x[::freq], ticks[::freq], rotation=0, ha='center')
        else:
            plt.xticks(x[::freq], ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        plt.ylabel('EAD ratio', fontsize=12)
        # Add legend
        plt.legend(loc='best', frameon=False)
        # Add horizontal lines
        plt.grid(axis='y', ls=':', lw=0.3)
        # Add title for the figure
        if self.sublevel == None or sublevel_in_title == False:
            plt.title(f'EAD Backtest results for the {order} year horizon ({weight.upper()})')
        else:
            plt.title(f'EAD Backtest results for the {order} year horizon ({weight.upper()}) - {self.sublevel.replace("_", " ").title()}')

        # Show and save the plot
        if self.sublevel == None:
            plt.savefig(newfolder + '/plots/EAD/' + 'EAD_CQ_1_' + weight + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            EAD_CQ_1_plots[len(EAD_CQ_1_plots)] = self.table_name
        else:
            plt.savefig(newfolder + '/plots/EAD/' + 'EAD_CQ_2_' + weight + '_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            EAD_CQ_2_plots[len(EAD_CQ_2_plots)] = self.table_name
        if show_plots == True:
            plt.show()
        plt.close()

# PSI value over time (not used anymore)
class PSI_PLOT:
    def __init__(self, table_name, weight):
        self.type = 'plot'
        self.table_name = table_name
        self.data = sas_output[table_name]
        self.weight = weight
        try:
            self.sublevel = self.table_name.split(weight + '_')[1].lower()
            if self.sublevel in ['all', 'oall']:
                self.sublevel = ''
        except:
            self.sublevel = ''

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]
        plt.rcParams['xtick.major.pad'] = 5

        weight = self.weight  # nw/ew

        x = np.arange(0, len(self.data.reporting_date))
        y = self.data['PSI'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        ticks = self.data['reporting_date']
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # Create the line plot for series PSI
        # plt.plot(x, y, ls = '-', lw = 2, color = '#007acc', alpha = 0.6)
        # plt.fill_between(x, y1=y, y2=0, color = '#007acc', alpha = 0.1)
        plt.plot(x, y, ls='-', lw=2, color='orangered', alpha=0.6)
        plt.fill_between(x, y1=y, y2=0, color='bisque', alpha=0.4)

        # Setting correct ticks for x axis
        # Rotation is necessary, without it the longer ticks get cut
        plt.xticks(x[::freq], ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        plt.ylabel('PSI value', fontsize=12)
        # Add legend
        # plt.legend(loc = 'best', frameon = False)
        # Add horizontal lines
        plt.grid(axis='y', ls=':', lw=0.3)
        # Add the threshold
        plt.axhline(y=0.1, xmin=0, xmax=len(self.data), color='grey', ls='--', lw=1)
        plt.axhline(y=0.25, xmin=0, xmax=len(self.data), color='grey', ls='--', lw=1)
        # Add title for the figure
        if self.sublevel == '' or sublevel_in_title == False:
            plt.title(f'PSI value over time ({weight.upper()})')
        else:
            plt.title(f'PSI value over time ({weight.upper()}) - {self.sublevel.replace("_", " ").title()}')

        # Show and save the plot
        plt.savefig(newfolder + '/plots/Others/' + 'PSI_' + weight + '_' + str(self.sublevel) + '_' + '.png', dpi = 300, bbox_inches = 'tight')
        others_plots[len(others_plots)] = self.table_name
        if show_plots == True:
            plt.show()
        plt.close()

# MCC and Type II error over time (Staging Model Output)
class DISCRIM_POWER_STAGE_PLOT:
    def __init__(self, table_name, horizon):
        self.type = 'plot'
        self.table_name = table_name
        self.horizon = 'horizon'
        self.mcc = 'mcc_nw'
        self.type_2_err = 'type2_error_nw'
        self.reporting_date = 'reporting_date'
        self.dataset = sas_output[table_name]
        self.data = self.dataset.loc[self.dataset[self.horizon] == horizon].copy()
        try:
            self.sublevel = self.table_name.split('discrim_power_stage_')[1].lower()
            if self.sublevel in ['all', 'oall']:
                self.sublevel = None
        except:
            self.sublevel = None

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]
        plt.rcParams['xtick.major.pad'] = 5
        if self.horizon == 0:
            order = 'first'
        elif self.horizon == 1:
            order = 'second'
        elif self.horizon == 2:
            order = 'third'
        elif self.horizon == 3:
            order = 'fourth'
        elif self.horizon == 4:
            order = 'fifth'

        x = np.arange(0, len(self.data[self.reporting_date]))
        y = self.data[self.mcc].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        y_2 = self.data[self.type_2_err].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        ticks = self.data[self.reporting_date]
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # define two y-axis
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        # plot
        ax1.plot(x, y, ls='-', lw=2, color='lightsteelblue', marker='o', ms=6, mfc='navy', alpha=0.8, label='MCC')
        ax2.plot(x, y_2, ls='-', lw=2, color='lightcoral', marker='o', ms=6, mfc='brown', alpha=0.6,
                 label='Type II error')

        # Setting correct ticks for x axis
        # Rotation is necessary, without it the longer ticks get cut
        if len(self.data) in range(1, 8):
            ax1.set_xticks(x[::freq])
            ax1.set_xticklabels(ticks[::freq], rotation=0, ha='center')
        else:
            ax1.set_xticks(x[::freq])
            ax1.set_xticklabels(ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        ax1.set_ylabel('MCC', fontsize=12)
        ax2.set_ylabel('Type II error', fontsize=12, rotation=270, labelpad=18)
        # Add legend
        lines = ax1.get_lines() + ax2.get_lines()
        ax1.legend(lines, [line.get_label() for line in lines], loc='best', frameon=False)
        # Add title for the figure
        if self.sublevel == None or sublevel_in_title == False:
            plt.title(f"MCC and Type II error over time")
        else:
            plt.title(f"MCC and Type II error over time - {self.sublevel.replace('_', ' ').title()}")

        # Show and save the plot
        if self.sublevel == None:
            plt.savefig(newfolder + '/plots/Staging/' + 'STAGING_DP_1' + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            STAGING_DP_1_plots[len(STAGING_DP_1_plots)] = self.table_name
        else:
            plt.savefig(newfolder + '/plots/Staging/' + 'STAGING_DP_2_' + str(self.sublevel) + '_' + str(self.horizon) + '.png', dpi = 300, bbox_inches = 'tight')
            STAGING_DP_2_plots[len(STAGING_DP_2_plots)] = self.table_name
        if show_plots == True:
            plt.show()
        plt.close()

# cure/no loss rate over time [NOT TESTED, MIGHT BE INCORRECT]
class CURE_PLOT:
    def __init__(self, table_name, weight, method = 'pit'):
        self.type = 'plot'
        self.table_name = table_name
        self.dataset = sas_output[table_name]
        self.data = self.dataset.loc[self.dataset.horizon == 0]
        self.method = method     # pit/ttc
        self.weight = weight

    def main_output(self):
        if self.data.empty:
            return None
        plt.rcParams['axes.edgecolor'] = 'dimgray'
        plt.rcParams['xtick.color'] = 'black'
        plt.rcParams['ytick.color'] = 'black'
        plt.style.use('seaborn-v0_8-pastel')
        plt.rcParams["figure.figsize"] = [9, 4.5]
        plt.rcParams['xtick.major.pad'] = 8

        weight = self.weight  # nw/ew
        if 'cure' in self.table_name:
            pred_var = f'{self.method}_cure_pred_{weight.upper()}'
            obs_var = 'cure_obs_NW'
            label_ = 'cure rate'
            if self.method == 'pit':
                way = 'PiT'
            elif self.method == 'ttc':
                way = 'TTC'
        elif 'noloss' in self.table_name:
            pred_var = f'{self.method}_cure_pred_{weight.upper()}'  # yes, the same pred_var as before
            obs_var = 'noloss_obs_NW'
            label_ = 'no loss rate'
            if self.method == 'pit':
                way = 'PiT'
            elif self.method == 'ttc':
                way = 'TTC'

        x = np.arange(0, len(self.data.reporting_date))
        y = self.data[pred_var].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        y_2 = self.data[obs_var].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        try:
            y_ub = self.data[f'UB_CR'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data[f'LB_CR'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        except:
            y_ub = self.data['UB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
            y_lb = self.data['LB'].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        ticks = self.data['reporting_date']
        freq = max(math.floor(len(self.data) / 18), 1)  # min.step = 1

        # Create the line plot for series Estimated value
        plt.plot(x, y, ls='--', lw=1.5, color='orangered', marker='D', ms=4, mfc='crimson', alpha=0.6,
                 label=f'Estimated {label_}')
        # Create shadow indicating CI
        plt.fill_between(x, y_lb, y_ub, color='mistyrose', alpha=0.5)
        # Add the line plot for series observed value
        plt.plot(x, y_2, ls='--', lw=1.5, color='grey', marker='D', ms=4, mfc='dimgrey', alpha=0.8,
                 label=f'Observed {label_}')

        # Setting correct ticks for x axis
        # Rotation is necessary, without it the longer ticks get cut
        if len(self.data) in range(1, 6):
            plt.xticks(x[::freq], ticks[::freq], rotation=0, ha='center')
        else:
            plt.xticks(x[::freq], ticks[::freq], rotation=60, ha='right')
        # Format y axis as percent
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # Add label for y-axis
        plt.ylabel(f'Estimated & Observed {label_}', fontsize=12)
        # Add legend
        plt.legend(loc='best', frameon=False)
        # Add horizontal lines
        plt.grid(axis='y', ls=':', lw=0.3)
        # Add title for the figure
        plt.title(f'Backtest results for {way} {label_} for the first year horizon ({weight.upper()})')

        # Show and save the plot
        plt.savefig(newfolder + '/plots/Others/' + 'cure_plot_' + self.method + '_' + weight + '.png', dpi = 300, bbox_inches = 'tight')
        others_plots[len(others_plots)] = self.table_name
        if show_plots == True:
            plt.show()
        plt.close()


#######################################################################################################################

### TABLES

class DISCRIM_POWER_TABLE:
    def __init__(self, table_name, var):
        self.type = 'table'
        self.data = sas_output[table_name].copy(deep=True)
        self.var = var
        self.result_var = 'result_test_' + self.var
        self.horizon = 'horizon'
        self.reporting_date = 'reporting_date'

    def main_output(self):
        if self.data is not None:
            data = self.data
            num_years = max(data[self.horizon]) + 1
            dates = data[self.reporting_date].unique()
            result_df = pd.DataFrame(columns=['Reporting Date'] + [f'Year {x}' for x in range(1, num_years + 1)])
            result_df['Reporting Date'] = dates
            for index, row in data.iterrows():
                result_df[f'Year {row[self.horizon] + 1}'][result_df['Reporting Date'] == row[self.reporting_date]] = (
                    f'{100 * row[self.var]:.0f}%')

            # for index, row in data.iterrows():
            #     result_df[f'Year {row[self.horizon] + 1}'][result_df['Reporting Date'] == row[self.reporting_date]] = (
            #         f'{100 * row[self.var]:.0f}% (#{"ffbdbd" if row[self.result_var] == "Fail" else "f0fae6"})')

            # return np.vstack((result_df.columns, result_df.to_numpy(na_value='')))

            result_df = result_df.fillna('  ')
            return result_df

class BACKTEST_PIT_TABLE:
    def __init__(self, backtest_table, misestimation_table):
        self.type = 'table'
        self.data_1 = sas_output[backtest_table].copy(deep=True)
        self.data_2 = sas_output[misestimation_table].copy(deep=True)
        self.colname_result = [x for x in self.data_1.columns[self.data_1.columns.str.contains('result')]][0]
        self.horizon_1 = 'horizon'
        self.horizon_2 = 'horizon'
        self.eur_mis_est = 'EUR_mis_est'
        self.perc_mis_est = 'Perc_mis_est'

    def main_output(self):
        self.data_1['horizon'] = self.data_1[self.horizon_1] + 1
        self.data_2['horizon'] = self.data_2[self.horizon_2] + 1
        acc_perc_horizon = self.data_1[self.colname_result].eq('Accurate').groupby(
            self.data_1.horizon).mean().reset_index()
        misest_info = self.data_2[['horizon', self.eur_mis_est, self.perc_mis_est]]
        result = acc_perc_horizon.merge(misest_info, on="horizon")

        if result[self.eur_mis_est].dtype == np.int64:
            result[self.eur_mis_est] = result[self.eur_mis_est].astype(float)
            result[self.perc_mis_est] = result[self.perc_mis_est].apply(lambda x: x.replace('%', '') if type(x) == str else x)
            result[self.perc_mis_est] = result[self.perc_mis_est].astype(float) / 100
        else:
            result[self.eur_mis_est] = result[self.eur_mis_est].apply(lambda x: x.replace(',', '') if type(x) == str else x)
            result[self.eur_mis_est] = result[self.eur_mis_est].astype(float)

            result[self.perc_mis_est] = result[self.perc_mis_est].apply(lambda x: x.replace('%', '') if type(x) == str else x)
            result[self.perc_mis_est] = result[self.perc_mis_est].astype(float) / 100

        acc_perc_total = self.data_1[self.colname_result].eq('Accurate').mean()
        mis_sum = result[self.eur_mis_est].sum()

        result['horizon'] = result['horizon'].apply(lambda x: f'Year {x}')
        # result = result.append({'horizon' : 'Overall', self.colname_result: acc_perc_total, 'EUR_mis_est':mis_sum } , ignore_index=True)
        result = pd.concat((result, pd.DataFrame({'horizon': 'Overall', self.colname_result: acc_perc_total,
                                                    self.eur_mis_est: mis_sum}, index=[0])), ignore_index=True)

        result = result.rename(columns={'horizon': 'Horizon', self.colname_result: '% Accurate per horizon',
                                        self.eur_mis_est: 'Difference outside bounds (EUR)',
                                        self.perc_mis_est: '% Outside bounds'})

        result[['% Accurate per horizon', '% Outside bounds']] = result[['% Accurate per horizon',
                                                                            '% Outside bounds']].map(
            "{0:.2%}".format)
        result[['Difference outside bounds (EUR)']] = result[['Difference outside bounds (EUR)']].map(
            "€{:,.0f}".format)
        result.loc[
            result.index[-1], '% Outside bounds'] = '  '  # set the last cell to empty (previously shown as nan%)

        # return np.vstack((result.columns, result.to_numpy(na_value='')))
        result = result.fillna('  ')
        return result

class GENERAL_BACKTEST_TTC_P1_TABLE:
    def __init__(self, table_name, weight):
        self.type = 'table'
        self.pred_var = 'LGD_pred_EW'
        self.obs_var = 'LGD_obs_EW'
        self.table_name = table_name
        self.weight = weight
        self.dataset = sas_output[self.table_name]
        self.data = self.dataset.loc[self.dataset.horizon == 0]

    def main_output(self):
        weight = self.weight  # nw/ew
        # seg = re.sub('[^A-Z]', '', self.table_name)  # PD/LGD/ECL
        # Define varaibles indicating predicted/observed values and set up labels
        if '_LGD_' in self.table_name:
            pred_var = f'LGD_pred_EW'
            obs_var = f'LGD_obs_EW'
            label_ = 'LGD'
        elif '_ECL_' in self.table_name:
            pred_var = 'ELR_mar'
            obs_var = 'OLR_mar'
            label_ = 'LR'
        elif '_PD_' in self.table_name:
            pred_var = f'{weight}_pit_prediction'
            obs_var = f'{weight}_odr'
            label_ = 'PD'

        df = pd.DataFrame()
        if 'reporting_date' in self.data.columns:
            df['Observation date'] = self.data.reporting_date
        elif 'REPORTING_DATE' in self.data.columns:
            df['Observation date'] = self.data.REPORTING_DATE
        else:
            pass
        df['Predicted'] = self.data[pred_var]
        df['Observed'] = self.data[obs_var]

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class GENERAL_BACKTEST_TTC_P2_TABLE:
    def __init__(self, table_name):
        self.data = sas_output[table_name]
        self.obs_mean = 'obs_mean'
        self.pred_mean = 'pred_mean'
        self.t_stat = 't_value'
        self.crit_val = 'crit_val'
        self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Average Observed'] = self.data[self.obs_mean]
        df['Average Predicted'] = self.data[self.pred_mean]
        df['t-Statistic'] = round(self.data[self.t_stat], 2)
        df['Critical value'] = round(self.data[self.crit_val], 2)
        df['Pass/Fail?'] = self.data[self.result]
        # df['color'] = np.where(df['Pass/Fail?'] == 'Pass', " (#ddf7bb)", " (#ffbdbd)")
        # df['Pass/Fail?'] = df['Pass/Fail?'] + df['color']
        # df.drop(['color'], axis=1, inplace=True)

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class BACKTEST_TTC_PD_RATING_TABLE:
    def __init__(self, table_name):
            self.data_1 = sas_output[table_name].sort_values('rating').reset_index(drop=True)
            self.t_stat = 't_value'
            self.crit_val = 'crit_val'
            self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Rating'] = self.data_1.rating
        if pd.api.types.is_string_dtype(self.data_1.obs_mean) is True:
            df['Average Observed DR'] = self.data_1.obs_mean
        else:
            df['Average Observed DR'] = ['{:.2%}'.format(i) for i in self.data_1.obs_mean]

        if pd.api.types.is_string_dtype(self.data_1.pred_mean) is True:
            df['Average predicted PD'] = self.data_1.pred_mean
        else:
            df['Average predicted PD'] = ['{:.2%}'.format(i) for i in self.data_1.pred_mean]

        df['t-Statistic'] = round(self.data_1[self.t_stat], 2)
        df['Critical value'] = round(self.data_1[self.crit_val], 2)
        df['Pass/Fail?'] = self.data_1[self.result]
        # df['color'] = np.where(df['Pass/Fail?'] == 'Pass', " (#ddf7bb)", " (#ffbdbd)")
        # df['Pass/Fail?'] = df['Pass/Fail?'] + df['color']
        # df.drop(['color'], axis=1, inplace=True)

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class MISEST_TTC_PD_RATING_TABLE:
    def __init__(self, table_name):
        self.data_1 = sas_output[table_name].sort_values('rating').reset_index(drop=True)
        # self.data_1 = self.data_1[self.data_1['result'] == 'Fail']
        self.rating = 'rating'
        self.total_ECL = 'total_ECL'
        self.mis_estimation = 'mis_estimation'

    def main_output(self):
        df = pd.DataFrame()
        df['Rating'] = self.data_1[self.rating]
        df['Total ECL'] = '€' + self.data_1[self.total_ECL]
        try:
            df['Mis-estimation'] = '€' + self.data_1[self.mis_estimation]
        except:
            df['Mis-estimation'] = '€' + self.data_1['final_misestimation']

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class PSI_TABLE:
    def __init__(self, table_name):
        self.data = sas_output[table_name].copy(deep=True)
        self.psi = 'PSI'

    def main_output(self):
        psi_value = self.data[self.psi].apply(lambda x: re.sub('[( %)]', '', x) if type(x) == str else x).astype('float') / 100.0
        avg_psi = psi_value.mean()
        max_psi = psi_value.max()
        list_psi = [avg_psi, max_psi]

        df = pd.DataFrame()
        df['Statistics'] = ['Average', 'Maximum value']
        df['PSI'] = ['{:.2%}'.format(i) for i in list_psi]

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class DISCRIM_POWER_STAGE_TABLE:
    def __init__(self, table_name):
        self.type = 'table'
        self.dataset = sas_output[table_name].copy(deep=True)
        # self.data = self.dataset.loc[self.dataset.horizon == 0]
        self.data = self.dataset
        self.reporting_date = 'reporting_date'
        self.horizon = 'horizon'
        self.mcc = 'mcc_nw'
        self.type_2_err = 'type2_error_nw'
        self.pval_mcc = 'mcc_p_value'
        self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Reporting date'] = self.data[self.reporting_date]
        df['Reporting date'] = pd.to_datetime(df['Reporting date'], format = '%d%b%Y')      # convert to datetime to sort correctly
        df['Horizon'] = 'Year ' + (self.data[self.horizon] + 1).astype(str)
        df['MCC (NW)'] = self.data[self.mcc]
        df['Type II error'] = self.data[self.type_2_err]
        # df['p-value MCC'] = self.data[self.pval_mcc]          # p-value is no longer calculated in MV7 tool

        df['MCC (NW) float'] = df['MCC (NW)'].apply(lambda x: float(re.sub('[( %)]', '', x)) if type(x) == str else x)
        df['Type II error float'] = df['Type II error'].apply(lambda x: float(re.sub('[( %)]', '', x)) if type(x) == str else x)
        
        if portfolio_type.upper() == 'RETAIL':
            df['Conclusion MCC'] = df['MCC (NW) float'].apply(lambda x: 'Green' if x >= 20
                                                                        else ('Red' if x <= 10
                                                                        else ('Yellow' if x < 20 and x > 10
                                                                        else '  ')))

            df['Conclusion Type II error'] = df['Type II error float'].apply(lambda x: 'Green' if x <= 40
                                                                                        else ('Red' if x >= 60
                                                                                        else ('Yellow' if x > 40 and x < 60
                                                                                        else '  ')))
        elif portfolio_type.upper() in ('WHOLESALE', 'SME', 'WHOLESALE/SME'):
            df['Conclusion MCC'] = df['MCC (NW) float'].apply(lambda x: 'Green' if x >= 30
                                                                        else ('Red' if x <= 15
                                                                        else ('Yellow' if x < 30 and x > 15
                                                                        else '  ')))

            df['Conclusion Type II error'] = df['Type II error float'].apply(lambda x: 'Green' if x <= 30
                                                                                        else ('Red' if x >= 40
                                                                                        else ('Yellow' if x > 30 and x < 40
                                                                                        else '  ')))
        else:
            raise Exception(f'Unknown portfolio type <{portfolio_type}>. Please check portfolio_type in parameters.py.')
        
        df = df.drop(['MCC (NW) float', 'Type II error float'], axis = 1)

        # df['color'] = np.where(df['Conclusion MCC'] == 'Pass', " (#ddf7bb)", " (#ffbdbd)")
        # df['Conclusion MCC'] = df['Conclusion MCC'] + df['color']
        # df.drop(['color'], axis=1, inplace=True)

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        df = df.sort_values(by=['Horizon', 'Reporting date'])
        df['Reporting date'] = df['Reporting date'].dt.strftime('%d%b%Y').str.upper()      # convert back to string for consistency with other tables
        return df

class DISCRIM_POWER_STAGE_CHANGE_TABLE:
    def __init__(self, table_name):
        self.type = 'table'
        self.dataset = sas_output[table_name].copy(deep=True)
        # self.data = self.dataset.loc[self.dataset.horizon == 0]
        self.data = self.dataset
        self.reporting_date = 'reporting_date'
        self.horizon = 'horizon'
        self.mcc = 'mcc_nw'
        self.type_2_err = 'type2_error_nw'
        self.pval_mcc = 'mcc_p_value'
        self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Reporting date'] = self.data[self.reporting_date]
        df['Reporting date'] = pd.to_datetime(df['Reporting date'], format = '%d%b%Y')      # convert to datetime to sort correctly
        df['Horizon'] = 'Year ' + (self.data[self.horizon] + 1).astype(str)
        df['MCC (NW)'] = self.data[self.mcc]
        df['MCC (NW) float'] = df['MCC (NW)'].apply(lambda x: float(re.sub('[( %)]', '', x)) / 100.0 if type(x) == str else x)

        df = df.sort_values(by=['Horizon', 'Reporting date'])
        df_0 = df.loc[df['Horizon'] == 'Year 1']

        df_new = pd.DataFrame(columns=['MCC (development)', 'MCC (most recent snapshot)', 'Relative change', 'Absolute change'])
        df_new['MCC (most recent snapshot)'] = [df_0.iloc[-1, 3]]

        df_new = df_new.fillna('XXX')
        return df_new

class CALIB_TTEST_2SP_STAGE_TABLE:
    def __init__(self, table_name, segment = None):
        self.table_name = table_name
        if segment == None:
            self.data = sas_output[table_name].copy(deep=True)
        else:
            self.data = sas_output[table_name].loc[sas_output[table_name]['segment'] == segment].copy(deep=True)
        # self.data = self.dataset.loc[self.dataset.horizon == 0]
        self.reporting_date = 'reporting_date'
        self.horizon = 'horizon'
        self.odr_st_1 = 'odr_nw1'
        self.odr_st_2 = 'odr_nw2'
        self.t_stat = 't_value_2'
        self.pval = 'p_value_t_2'
        self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Reporting date'] = self.data[self.reporting_date]
        df['Horizon'] = 'Year ' + (self.data[self.horizon] + 1).astype(str)
        df['Stage 1 ODR'] = self.data[self.odr_st_1].apply(lambda x: f'{x:.2%}')
        df['Stage 2 ODR'] = self.data[self.odr_st_2].apply(lambda x: f'{x:.2%}')
        df['t-Statistic'] = round(self.data[self.t_stat], 1)
        df['p-value'] = round(self.data[self.pval], 2)
        df['Conclusion'] = self.data[self.result]
        df['Conclusion'] = df['Conclusion'].apply(lambda x: 'Fail' if x == 'Fails' else ('  ' if x == '.' else 'Pass'))
        # df['color'] = np.where(df['Conclusion'] == 'Pass', " (#ddf7bb)", " (#ffbdbd)")
        # df['Conclusion'] = df['Conclusion'] + df['color']
        # df.drop(['color'], axis=1, inplace=True)

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class CALIB_TTEST_1SP_STAGE_TABLE:
    def __init__(self, table_name, segment = None):
        self.table_name = table_name
        if segment == None:
            self.data = sas_output[table_name].copy(deep=True)
        else:
            self.data = sas_output[table_name].loc[sas_output[table_name]['segment'] == segment].copy(deep=True)
        # self.data = self.dataset.loc[self.dataset.horizon == 0]
        self.reporting_date = 'reporting_date'
        self.horizon = 'horizon'
        self.odr = 'odr_nw'
        self.pd_at_origination = 'pd_pit_at_orig_date_av'
        self.t_stat = 't_value_1'
        self.pval = 'p_value_t_1'
        self.result = 'result'

    def main_output(self):
        df = pd.DataFrame()
        df['Reporting date'] = self.data[self.reporting_date]
        df['Horizon'] = 'Year ' + (self.data[self.horizon] + 1).astype(str)
        df['Stage 2 ODR'] = self.data[self.odr].apply(lambda x: f'{x:.2%}')
        df['PD at origination'] = self.data[self.pd_at_origination].apply(lambda x: f'{x:.2%}')
        df['t-Statistic'] = round(self.data[self.t_stat], 1)
        df['p-value'] = round(self.data[self.pval], 2)
        df['Conclusion'] = self.data[self.result]
        df['Conclusion'] = df['Conclusion'].apply(lambda x: 'Fail' if x == 'Fails' else ('  ' if x == '.' else 'Pass'))
        # df['color'] = np.where(df['Conclusion'] == 'Pass', " (#ddf7bb)", " (#ffbdbd)")
        # df['Conclusion'] = df['Conclusion'] + df['color']
        # df.drop(['color'], axis=1, inplace=True)

        # return np.vstack((df.columns, df.to_numpy(na_value='')))
        df = df.fillna('  ')
        return df

class PROVISIONS:
    def __init__(self, table_name):
        self.table_name = table_name
        self.data = sas_output[table_name].copy(deep=True)
        self.reporting_date = 'reporting_date'

    def main_output(self):
        # make sure the columns are in the order of: reporting_date, IFRS_stage, PROVISION_CATEGORY, horizon, Total_ECL
        if self.data is not None:
            df = self.data
            data = df[df.iloc[:, 2] == 'COLLECTIVE']
            max_horizon = 3  # aggregate beyond
            reporting_date = data[self.reporting_date][0]
            stagecol = f'Provision as of {reporting_date}'
            matcol = f'Year {max_horizon + 2} to maturity'
            result_df = pd.DataFrame(columns=[stagecol] +
                                             [f'Year {x}' for x in range(1, max_horizon + 2)] +
                                             [matcol])
            result_df[stagecol] = ['Stage 1', 'Stage 2', 'Stage 1+2', 'Stage 3', 'Total']
            result_df.fillna(0, inplace=True)
            for index, row in data.iterrows():
                col = f'Year {row.iloc[3] + 1}' if row.iloc[3] <= max_horizon else matcol
                result_df[col] = result_df[col].astype(float)
                if isinstance(df.iloc[1, -1], float) or isinstance(df.iloc[1, -1], np.int64):
                    val = row.iloc[-1]
                else:
                    val = float(row.iloc[-1].replace(',', ''))
                result_df.loc[result_df[stagecol] == f'Stage {row.iloc[1]}', col] += val
                if row.iloc[1] in [1, 2]:
                    result_df.loc[result_df[stagecol] == 'Stage 1+2', col] += val
                result_df.loc[result_df[stagecol] == 'Total', col] += val

            result_df.loc[:, result_df.columns != stagecol] = result_df.loc[:, result_df.columns != stagecol].map(
                lambda x: f'€{x:,.0f}')
            
            # return np.vstack((result_df.columns, result_df.to_numpy(na_value='')))
            result_df = result_df.fillna('  ')
            return result_df

