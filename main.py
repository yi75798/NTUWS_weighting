#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   main.py
# Time    :   2022/06/15 16:56:33
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : Main program of Weighting program.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from weighting import weighting
import pandas as pd
import numpy as np

### Load the data
rawdata_path = 'testdata.csv' # The path of rawdata.
df = pd.read_csv(rawdata_path, encoding='utf_8_sig') 

### Post-stratification
output_path = os.getcwd() # Output directory
output_name = 'data_post_weighted.csv' # Output data name

df = weighting(df, population_path='population.xlsx').post_stratification()
df.to_csv(os.path.join(output_path, output_name), encoding='utf_8_sig', index=False)

### Raking
output_path = os.getcwd() # Output directory
output_name = 'data_raking_weighted.csv' # Output data name

df = weighting(df, population_path='population.xlsx').raking()
df.to_csv(os.path.join(output_path, output_name), encoding='utf_8_sig', index=False)

