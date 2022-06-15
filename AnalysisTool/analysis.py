#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   analysis.py
# Time    :   2022/03/31 15:00:54
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : Analysis tool for master thesis. Include frequency table, cross table,
#               regression model and plot.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel

#matplotlib.rcParams.update(_VSCode_defaultMatplotlib_Params)

## Rounding
def rounding(num, decimal=0):
    num = np.round(num, decimal)
    #num = float(num)
    return num


class Table:
    def __init__(self, data):
        '''
        :data (pandas.Dataframe)
        '''
        self.df = data
    
    def freq(self, var:str, w=None, label=None):
        '''
        Frequency distribution table.

        :var (str): The variable want to inspect frequency distribution.
        :w (str): Optional.
                  The column which will be used to weighted by.
                  Defult=None.
        :label (lsit): Optional.
                       The label of the values
        
        :return : pd.DataFrame
        '''
        df = self.df
        if w:
            a = pd.Series(df[[var, w]].groupby(var).sum()[w]) / df[w].sum()
            if label:
                b = label
            else:
                b = a.index
            c = np.round(a.values, 2)
            d = rounding(df[[var, w]].groupby(var).sum()[w])
            df_temp = pd.DataFrame({'Label': b, 'Num': d, 'Freq': c})
            return df_temp
        else:
            df[w] = 1
            a = pd.Series(df[[var, w]].groupby(var).sum()[w]) / df[w].sum()
            if label:
                b = label
            else:
                b = a.index
            c = np.round(a.values, 2)
            d = rounding(df[[var, w]].groupby(var).sum()[w])
            df_temp = pd.DataFrame({'Label': b, 'Num': d, 'Freq': c})
            return df_temp
    
    def cross(self, r_var: str, c_var: str, w= None, percent_by='row'):
        '''
        Cross Table.

        : r_var (str): The variable of row.
        : c_var (str): The variable of column.

        : return : pd.DataFrame
        '''
        df = self.df
        if w:
            if percent_by == 'row':
                df_num = pd.crosstab(df[r_var], df[c_var], values=df[w], aggfunc=sum,
                                    margins=True).round(0).astype(int)
                df_freq = pd.crosstab(df[r_var], df[c_var], values=df[w], aggfunc=sum,
                                     margins=True,
                                     normalize='index').round(2)
                df_cross = pd.merge(df_num, df_freq, on=r_var, suffixes=['_nums', '_rfreq'])
                return df_cross
            elif percent_by== 'col':
                df_num = pd.crosstab(df[r_var], df[c_var], values=df[w], aggfunc=sum,
                                     margins=True).round(0).astype(int)
                df_freq = pd.crosstab(df[r_var], df[c_var],
                                     margins=True,
                                     normalize='columns').round(2)
                df_cross = pd.merge(df_num, df_freq, on=r_var, suffixes=['_nums', '_cfreq'])
                return df_cross
        else:
            if percent_by == 'row':
                df_num = pd.crosstab(df[r_var], df[c_var],
                                     margins=True)
                df_freq = pd.crosstab(df[r_var], df[c_var],
                                     margins=True,
                                     normalize='index').round(2)
                df_cross = pd.merge(df_num, df_freq, on=r_var, suffixes=['_nums', '_rfreq'])
                return df_cross
            elif percent_by== 'col':
                df_num = pd.crosstab(df[r_var], df[c_var],
                                     margins=True)
                df_freq = pd.crosstab(df[r_var], df[c_var],
                                     margins=True,
                                     normalize='columns').round(2)
                df_cross = pd.merge(df_num, df_freq, on=r_var, suffixes=['_nums', '_cfreq'])
                return df_cross

class Regression:
    def __init__(self, data, DV: str, IV: list, CV=[], method='OLS'):
        '''
        Bulid up a regression model.

        : data (pandas.DataFrame): Data for the model.
        : DV (str): Dependent variable.
        : IV (list): Independent variables.
        : CV (list): Optional. Control variables. Defalt = []
        : method (str): Method of fit the model.
                        Include OLS, Logit, Order.
                        Defalt = 'OLS'
        '''
        y = data[DV]
        x = data[IV+CV]
        if method == 'OLS':
            x = sm.add_constant(x)
            self.result = sm.OLS(y, x).fit()
        
        if method == 'Logit':
            x = sm.add_constant(x)
            self.result = sm.Logit(y, x).fit()
        
        if method == 'Order':
            self.result = OrderedModel(y, x, distr='probit').fit(method='bfgs')
    
    def coef(self):
        '''
        Turn regression model into the form for coeffient plot.

        : return : pd.DataFrame
        '''
        df = pd.DataFrame(self.result.summary().tables[1].data)
        df.columns = df.iloc[0]
        df = df.drop(0)
        df = df.set_index(df.columns[0])
        df = df.astype(float)
        df['errors'] = df['coef'] - df['[0.025']

        try:
            df =df.drop(['const'])
        except:
            pass
        try:
            df = df.drop(['1.0/2.0', '2.0/3.0', '3.0/4.0'])
        except:
            pass

        return df


class Coef_Plot:
    def __init__(self, data: list):
        '''
        Pick up the models to be plotted.

        :data: List of pd.DataFrame from the return of object Regression.coef().
        '''
        plt.style.use('seaborn')
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        sns.set_context('poster')
        
        if type(data) == list:
            self.data = data
        else:
            self.data = [data]
    
    def single_model(self, data_ord= 0, title=None,
                     colors = 'royalblue',
                     ylabel='coef.'):
        '''
        Coefficient plot of one regression model.

        :data_ord (int): Optional.
                         Order of the model in the list of Coef_Plot wanted to be plot.
                         Defult=0, eg. plot the first model.
        :title (str): Title of the figure. Defult=None.
        :colors (str): Color of the elements. Defult='royalblue'.
        :ylabel (str): Label of y-axis. Defult=coef.
        '''
        plt.figure(figsize=(8, 6), dpi= 300, facecolor = 'w')
        
        df = self.data[data_ord]
        plt.bar(df.index, df['coef'], color='none',
                yerr= df['errors'], ecolor= colors)
        plt.scatter(range(0, len(df['coef'])), df['coef'], color=colors, marker='o', s=80)

        plt.axhline(y= 0, color='silver', linestyle='--', linewidth=4)

        plt.xticks(rotation=90, fontsize=18)
        plt.xticks(fontsize=18)
        plt.title(title, fontsize=24)
        plt.ylabel(ylabel, fontsize=12)

        plt.show()
    
    def multi_year(self, IV: str, title=None,
                   label=None,
                   colors='royalblue',
                   ylabel='coef.', legend_loc='upper right'):
        '''
        Figure about the change of coef in 2008~2020.

        :IV (str): The variable of observation.
        :title (str): Title of the figure. Defult=None.
        :label (str): Label of the IV. Defult=None.
        :colors (str): Color of the elements. Defult='royalblue'.
        :ylabel (str): Label of y-axis. Defult=coef.
        :legend_loc (str): Location of legend. Defult='upper right'.
        '''
        plt.figure(figsize=(8, 6), dpi=300, facecolor='w')

        model = self.data
        if len(model) != 4: # The Coef_plot object must have 4 models or it wont work subsequently.
            return print('Error! The Coef_plot object must have 4 models.')

        x = [2008, 2012, 2016, 2020]
        y = [m.loc[IV]['coef'] for m in model]
        
        err = [m.loc[IV]['errors'] for m in model]

        plt.bar(x, y, color='none',
                yerr= err, ecolor= colors)
        plt.scatter(x, y, color=colors, marker='o', s=80)
        plt.plot(x, y, color=colors, label=label)

        plt.axhline(y= 0, color='silver', linestyle='--', linewidth=4)

        plt.xticks(x, rotation=90, fontsize=18)
        plt.title(title, fontsize=24)
        plt.ylabel(ylabel, fontsize=12)

        if label:
            plt.legend(loc=legend_loc, fontsize=12)

        plt.show()
    
    def multi_year_2model(self, iv1: str, iv2: str, title=None,
                          label1=None, label2=None, c1='royalblue', c2='m', 
                          ylabel='coef.', legend_loc='upper right'):
        '''
        Plot two variables for comparision.

        :iv1 (str): Variable1 to be compared.
        :iv2 (str): Variable2 to be compared.
        :label1 (str): Label of the IV1. Defult=None.
        :label2 (str): Label of the IV2. Defult=None.
        :c1 (str): Color of the IV1. Defult='royalblue'.
        :c2 (str): Color of the IV2. Defult='magenta'.
        :ylabel (str): Label of y-axis. Defult=coef.
        :legend_loc (str): Location of legend. Defult='upper right'.
        '''
        
        model = self.data
        plt.figure(figsize=(8, 6), dpi=300, facecolor='w')

        x = [2008, 2012, 2016, 2020]
        y1 = [m.loc[iv1]['coef'] for m in model]
        y2 = [m.loc[iv2]['coef'] for m in model]
        err1 = [m.loc[iv1]['errors'] for m in model]
        err2 = [m.loc[iv2]['errors'] for m in model]

        plt.bar(x, y1, color='none',
                yerr= err1, ecolor= c1)
        plt.scatter(x, y1, color=c1, marker='o', s=80, label=label1)
        plt.plot(x, y1, color=c1)        

        plt.bar([i + 0.5 for i in x], y2, color='none',
                yerr= err2, ecolor= c2)
        plt.scatter([i + 0.5 for i in x], y2, color=c2, marker='o', s=80, label=label2)
        plt.plot([i + 0.5 for i in x], y2, color=c2)   
        plt.axhline(y= 0, color='silver', linestyle='--', linewidth=4)
        plt.legend(loc='lower right', fontsize=14)
        plt.xticks(x, fontsize=18)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=24)
        plt.legend(loc=legend_loc, fontsize=12)

        plt.show()

if __name__ == '__main__':
    data = pd.read_csv('modeldata.csv')
    d2008 = data[data.year==2008]
    d2012 = data[data.year==2012]
    d2016 = data[data.year==2016]
    d2020 = data[data.year==2020]
    cv = ['ex_effi', 'in_effi',
         'engage', 'trust', 'SEX', 'AGE']
    df = Table(d2020)
    freq = df.freq('d_sat')
    display(freq)

    cross = df.cross('d_sat', 'NPID', percent_by='row', w='weight')
    display(cross)

    m2008 = Regression(d2008, 'd_sup', ['N_kmt', 'N_dpp'], CV=cv, method='Logit')
    m2012 = Regression(d2012, 'd_sup', ['N_kmt', 'N_dpp'], CV=cv, method='Logit')
    m2016 = Regression(d2016, 'd_sup', ['N_kmt', 'N_dpp'], CV=cv, method='Logit')
    m2020 = Regression(d2020, 'd_sup', ['N_kmt', 'N_dpp'], CV=cv, method='Logit')
    print(m2008.result.summary())
    coef2008 = m2008.coef()
    coef2012 = m2012.coef()
    coef2016 = m2016.coef()
    coef2020 = m2020.coef()

    plot_model = Coef_Plot([m2008.coef(), m2012.coef(), m2016.coef(), m2020.coef()])

    plot_model.single_model(title='(Ex. single_model) DV: d_sup')
    plot_model.multi_year(IV='N_dpp', title='(Ex. multi_year) DV: d_sup', label='IV: N_dpp')
    plot_model.multi_year_2model(iv1='N_kmt',
                                  iv2='N_dpp',
                                  title='(Ex. multi_y 2m) DV: d_sup',
                                  label1='N_kmt',
                                  label2='N_dpp')