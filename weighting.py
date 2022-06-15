#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   weighting.py
# Time    :   2022/06/15 10:29:30
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : Weighting program include Post-stratification and Raking

import pandas as pd
import numpy as np
from AnalysisTool.analysis import *

# def chitest(obs, exp)

class weighting:
    def __init__(self, data, population_path='population.xlsx'):
        '''
        Build up a weighting machine.
        ---------------------------------
        :param data(pandas.DataFrame): The data wnat to be weight.
        :param population_path(str): Optinal.
                                     The path of the population data.
                                     Defalt='population.xlsx'.
        '''
        self.df = data.copy()
        self.N_SAA = pd.read_excel(population_path, sheet_name='SAA', index_col='index')
        self.N_SEX = pd.read_excel(population_path, sheet_name='SEX', index_col='Value')
        self.N_AGE = pd.read_excel(population_path, sheet_name='AGE', index_col='Value')
        self.N_EDU = pd.read_excel(population_path, sheet_name='EDU', index_col='Value')
        self.N_AREA = pd.read_excel(population_path, sheet_name='AREA', index_col='Value')
    
    def stratified(self):
        self.df['strata'] = None
        for i in self.df.index:
            if self.df['SEX'].loc[i] != -1:
                sex = str(self.df['SEX'].loc[i])
            else:
                sex = ''

            if self.df['AGE'].loc[i] != -1:
                age = str(self.df['AGE'].loc[i])
            else:
                age = '' 
            
            if self.df['AREA'].loc[i] != -1:
                area = str(self.df['AREA'].loc[i])
            else:
                area = ''
            
            strata_index = int(sex+age+area)
            try:
                self.df['strata'].loc[i] = self.N_SAA['group'].loc[strata_index]
            except:
                self.df['strata'].loc[i] = None
    
    def post_stratification(self, weight_col_name='weight'):
        '''
        Weight by post-stratification.
        -------------------------------
        :param weight_col_name(str): Optional.
                                     The name of the column of weight.
                                     Defalt='weight'
        :return pandas.Dataframe with weight values column.                             
        '''
        self.stratified() 
        self.df[weight_col_name] = 1
        self.N_SAA = self.N_SAA.set_index('group')
        n = len(self.df)
        for i in self.df.index:
            strata = self.df['strata'].loc[i]
            Ni_N = self.N_SAA['ratio'].loc[strata]
            n_ni = (n/len(self.df[self.df['strata'] == strata]))

            w = Ni_N * n_ni
            self.df[weight_col_name].loc[i] = w
        
        return self.df

if __name__ == '__main__':
    data = pd.read_csv('data.csv', encoding='utf_8_sig')
    dfw = weighting(data)
    dfw = dfw.post_stratification()
    
            






    

