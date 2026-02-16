####################################################################################################################
### This is the executable file to run the program. It will import the main file from the src folder and run it. ###
####################################################################################################################

print("####################################################")
print("############## IFRS9 Output Generator ##############")
print("#################### Version 0.2 ###################")
print("############# Last updated: 22/11/2024 #############")
print("####################################################")
print("################# Created by Tú Vû #################")
print("################### tu.vu@ing.com ##################")
print("####################################################\n\n")

print("If something is not working properly, please read the README file and any error messages that appear below.\nOtherwise, please contact @Vû, X.T. (Tú).\n\n")

print("#####################################")
print("Running the IFRS9 Output Generator...")
print("#####################################\n")

### Importing all dependencies (including the ones in the source files)
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import re

### Executing the main file in the source code (source code remains editable)
import os
import sys
import traceback

path = os.getcwd()
sys.path.append(path + "/src")
sys.path.insert(1, path + '/_internal/src')

### Error handling
def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    os.system('pause')
    sys.exit(-1)

sys.excepthook = show_exception_and_exit

## Execute the main file
import main

## Pause the program before closing the console to allow the user to read the output
os.system('pause')

