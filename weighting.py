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
from scipy.stats import chisquare

class weighting:
    def __init__(self, data, population_path='population.xlsx', weight_col_name='weight'):
        '''
        Build up a weighting machine.
        ---------------------------------
        :param data(pandas.DataFrame): The data wnat to be weight.
        :param population_path(str): Optinal.
                                     The path of the population data.
                                     Defalt='population.xlsx'.
        :param weight_col_name(str): Optional.
                                     The name of the column of weight.
                                     Defalt='weight'                             
        '''
        self.df = data.copy()
        self.df[weight_col_name] = 1
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
    
    def post_stratification(self, weight_col='weight'):
        '''
        Weight by post-stratification.
        -------------------------------
        :param weight_col(str): Optional.
                                The name of the column of weight.
                                Defalt='weight'
        :return pandas.Dataframe with weight values column.                             
        '''
        self.stratified() 
        self.N_SAA = self.N_SAA.set_index('group')
        n = len(self.df)
        for i in self.df.index:
            strata = self.df['strata'].loc[i]
            Ni_N = self.N_SAA['ratio'].loc[strata]
            n_ni = (n/len(self.df[self.df['strata'] == strata]))

            w = Ni_N * n_ni
            self.df[weight_col].loc[i] = w
        
        return self.df
    def chitest(self, var, w_col= 'weight', message=False):
        '''
        Chi-square test.
        ------------------
        :param var(str): Variable to test.
        :param w_col(str): Optional.
                           The column of the weight.
        :param message(bool): Whether to print the test result.
        :return Bool.
        '''
        obs = Table(self.df[self.df[var] != -1]).freq(var, w=w_col)['Num'].values
        n = rounding(self.df[self.df[var] != -1][w_col].sum())
        if var == 'SEX':
            exp = np.array(n * self.N_SEX['ratio'])
            chi, p = chisquare(f_obs= obs, f_exp= exp, ddof= 0)

            if message:    
                print(f'chi2= {chi}, p = {p}')
                if p >= 0.05:
                    print('SEX consistent with population.')
                    return True
                else:
                    print('SEX inconsistent with population.')
                    return False
            else:
                if p >= 0.05:
                    return True
                else:
                    return False
        if var == 'AGE':
            exp = np.array(n * self.N_AGE['ratio'])
            chi, p = chisquare(f_obs= obs, f_exp= exp, ddof= 0)

            if message:    
                print(f'chi2= {chi}, p = {p}')
                if p >= 0.05:
                    print('AGE consistent with population.')
                    return True
                else:
                    print('AGE inconsistent with population.')
                    return False
            else:
                if p >= 0.05:
                    return True
                else:
                    return False
        if var == 'EDU':
            exp = np.array(n * self.N_EDU['ratio'])
            chi, p = chisquare(f_obs= obs, f_exp= exp, ddof= 0)

            if message:    
                print(f'chi2= {chi}, p = {p}')
                if p >= 0.05:
                    print('EDU consistent with population.')
                    return True
                else:
                    print('EDU inconsistent with population.')
                    return False
            else:
                if p >= 0.05:
                    return True
                else:
                    return False
        if var == 'AREA':
            exp = np.array(n * self.N_AREA['ratio'])
            chi, p = chisquare(f_obs= obs, f_exp= exp, ddof= 0)

            if message:    
                print(f'chi2= {chi}, p = {p}')
                if p >= 0.05:
                    print('AREA consistent with population.')
                    return True
                else:
                    print('AREA inconsistent with population.')
                    return False
            else:
                if p >= 0.05:
                    return True
                else:
                    return False

    def rake_sex(self, weight_col='weight'):
        #W = self.df[weight_col].loc[i]
        n = rounding(self.df[self.df['SEX'] != -1][weight_col].sum())
        n0 = Table(self.df).freq('SEX', w=weight_col)['Num'].loc[0]
        n1 = Table(self.df).freq('SEX', w=weight_col)['Num'].loc[1]
        N0 = self.N_SEX['ratio'].loc[0]
        N1 = self.N_SEX['ratio'].loc[1]
        for i in self.df.index:
            W = self.df[weight_col].loc[i]
            if self.df['SEX'].loc[i] == 0:
                self.df[weight_col].loc[i] = W * N0 * n/n0
            elif self.df['SEX'].loc[i] == 1:
                self.df[weight_col].loc[i] = W * N1 * n/n1

    
    def rake_age(self, weight_col='weight'):
        #W = self.df[weight_col].loc[i]
        n = rounding(self.df[self.df['AGE'] != -1][weight_col].sum())
        n1 = Table(self.df).freq('AGE', w=weight_col)['Num'].loc[1]
        n2 = Table(self.df).freq('AGE', w=weight_col)['Num'].loc[2]
        n3 = Table(self.df).freq('AGE', w=weight_col)['Num'].loc[3]
        n4 = Table(self.df).freq('AGE', w=weight_col)['Num'].loc[4]
        n5 = Table(self.df).freq('AGE', w=weight_col)['Num'].loc[5]
        N1 = self.N_AGE['ratio'].loc[1]
        N2 = self.N_AGE['ratio'].loc[2]
        N3 = self.N_AGE['ratio'].loc[3]
        N4 = self.N_AGE['ratio'].loc[4]
        N5 = self.N_AGE['ratio'].loc[5]
        
        for i in self.df.index:
            W = self.df[weight_col].loc[i]
            if self.df['AGE'].loc[i] == 1:
                self.df[weight_col].loc[i] = W * N1 * n/n1
            elif self.df['AGE'].loc[i] == 2:
                self.df[weight_col].loc[i] = W * N2 * n/n2
            elif self.df['AGE'].loc[i] == 3:
                self.df[weight_col].loc[i] = W * N3 * n/n3
            elif self.df['AGE'].loc[i] == 4:
                self.df[weight_col].loc[i] = W * N4 * n/n4
            elif self.df['AGE'].loc[i] == 5:
                self.df[weight_col].loc[i] = W * N5 * n/n5
    
    def rake_edu(self, weight_col='weight'):
        #W = self.df[weight_col].loc[i]
        n = rounding(self.df[self.df['EDU'] != -1][weight_col].sum())
        n1 = Table(self.df).freq('EDU', w=weight_col)['Num'].loc[1]
        n2 = Table(self.df).freq('EDU', w=weight_col)['Num'].loc[2]
        n3 = Table(self.df).freq('EDU', w=weight_col)['Num'].loc[3]
        n4 = Table(self.df).freq('EDU', w=weight_col)['Num'].loc[4]
        n5 = Table(self.df).freq('EDU', w=weight_col)['Num'].loc[5]
        N1 = self.N_EDU['ratio'].loc[1]
        N2 = self.N_EDU['ratio'].loc[2]
        N3 = self.N_EDU['ratio'].loc[3]
        N4 = self.N_EDU['ratio'].loc[4]
        N5 = self.N_EDU['ratio'].loc[5]
        
        for i in self.df.index:
            W = self.df[weight_col].loc[i]
            if self.df['EDU'].loc[i] == 1:
                self.df[weight_col].loc[i] = W * N1 * n/n1
            elif self.df['EDU'].loc[i] == 2:
                self.df[weight_col].loc[i] = W * N2 * n/n2
            elif self.df['EDU'].loc[i] == 3:
                self.df[weight_col].loc[i] = W * N3 * n/n3
            elif self.df['EDU'].loc[i] == 4:
                self.df[weight_col].loc[i] = W * N4 * n/n4
            elif self.df['EDU'].loc[i] == 5:
                self.df[weight_col].loc[i] = W * N5 * n/n5
    
    def rake_area(self, weight_col='weight'):
        #W = self.df[weight_col].loc[i]
        n = rounding(self.df[self.df['AREA'] != -1][weight_col].sum())
        n1 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[1]
        n2 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[2]
        n3 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[3]
        n4 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[4]
        n5 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[5]
        n6 = Table(self.df).freq('AREA', w=weight_col)['Num'].loc[6]
        N1 = self.N_AREA['ratio'].loc[1]
        N2 = self.N_AREA['ratio'].loc[2]
        N3 = self.N_AREA['ratio'].loc[3]
        N4 = self.N_AREA['ratio'].loc[4]
        N5 = self.N_AREA['ratio'].loc[5]
        N6 = self.N_AREA['ratio'].loc[6]
        
        for i in self.df.index:
            W = self.df[weight_col].loc[i]
            if self.df['AREA'].loc[i] == 1:
                self.df[weight_col].loc[i] = W * N1 * n/n1
            elif self.df['AREA'].loc[i] == 2:
                self.df[weight_col].loc[i] = W * N2 * n/n2
            elif self.df['AREA'].loc[i] == 3:
                self.df[weight_col].loc[i] = W * N3 * n/n3
            elif self.df['AREA'].loc[i] == 4:
                self.df[weight_col].loc[i] = W * N4 * n/n4
            elif self.df['AREA'].loc[i] == 5:
                self.df[weight_col].loc[i] = W * N5 * n/n5
            elif self.df['AREA'].loc[i] == 6:
                self.df[weight_col].loc[i] = W * N6 * n/n6
    
    def raking(self, w_col='weight', var = ['SEX', 'AGE', 'EDU', 'AREA']):
        # chilist = [self.chitest(v, w_col=w_col) for v in var]

        r = 1
        while not all([self.chitest(v, w_col=w_col) for v in var]):
            print(f'第{r}輪加權')
            if ('SEX' in var) & (self.chitest('SEX') == False):
                self.rake_sex()
                r += 1
                continue
            if ('AGE' in var) & (self.chitest('AGE') == False):
                self.rake_age()
                r += 1
                continue
            if ('EDU' in var) & (self.chitest('EDU') == False):
                self.rake_edu()
                r += 1
                continue
            if ('AREA' in var) & (self.chitest('AREA') == False):
                self.rake_area()
                r += 1
                continue
            
        print(f'Raking至第{r-1}輪收斂')
        return self.df
      

if __name__ == '__main__':
    data = pd.read_csv('testdata.csv', encoding='utf_8_sig')
    dfw = weighting(data)
    dfw.chitest('AGE', message=True)

    dfw = dfw.post_stratification()
    dfw = dfw.raking()
    dfw['weight'].sum()
    

    
    
    