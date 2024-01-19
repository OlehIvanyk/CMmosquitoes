import pandas as pd
import numpy as np

import warnings

def cor_w(df):
# Розрахунок коефіцієнтів кореляції між параметрами
    name_col = ['Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb', 'Heat', 'Cool', 'PrecipTotal', 'StnPressure',
            'ResultSpeed', 'ResultDir', 'AvgSpeed', 'SeaLevel', 'Latitude', 'Longitude']

    df_name = df[name_col]
    df_cor = df_name.corr()
    return  df_cor

# warnings.filterwarnings('ignore')

# Коефіцієнти кореляції між параметрамих для даних без дублікатів рядків
name_wnv =['WnvPresent','Tmax',  'DewPoint',  'Heat',  'PrecipTotal', 'StnPressure',
                       'ResultSpeed', 'ResultDir','Latitude', 'Longitude']

data_pr = pd.read_csv('D:\Project_classific\cls_data.csv')
corr_data = cor_w(data_pr)
corr_data.to_excel('D:\Project_classific\cls_corr.xlsx')
# З data_pr видалені 'Tmin', 'Tavg','WetBulb','Cool','SeaLevel','AvgSpeed'які мають з іншими параметрами коефіцієнти
# кореляції > 0,8
data_pr = data_pr[name_wnv]
# Фрейм даних для моделювання (без дублікатів рядків)
data_pr.to_csv('D:\Project_classific\cls_wnv_mod.csv',index = False)
data_pr.to_excel('D:\Project_classific\cls_wnv_mod.xlsx',index = False)
# Коефіцієнти кореляції між параметрами для даних з дублікатами рядків

data_pr = pd.read_csv('D:\Project_classific\cls_dubl_data.csv')
corr_data = cor_w(data_pr)
corr_data.to_excel('D:\Project_classific\cls_dubl_corr.xlsx')
# З data_pr видалені 'Tmin', 'Tavg','WetBulb','Cool','SeaLevel','AvgSpeed'які мають з іншими параметрами коефіцієнти
# кореляції > 0,8
data_pr = data_pr[name_wnv]

# Фрейм даних для моделювання (з дублікатами рядків)
data_pr.to_csv('D:\Project_classific\cls_wnv_dubl_mod.csv',index = False)






