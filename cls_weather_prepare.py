import pandas as pd
import numpy as np

'''Підготовка даних з фреймів weather.csv та train.csv:
    - відбір даних, які будуть використовуватись в моделі

weather.csv:
'Station', 'Date', 'Tmax', 'Tmin', 'Tavg','DewPoint', 'WetBulb', 'Heat', 'Cool',  'PrecipTotal',
'StnPressure', 'ResultSpeed', 'ResultDir', 'AvgSpeed', 'SeaLevel'

train.csv
'Date", 'NumMosquitos', ''WnvPresent', 'Latitude', 'Longitude'

   - визначення типів даних
   - пошук та заміна даних, які не відносятьсяя до типів 'int' ,'float' np.int64, np.float64 в weather.csv:
      якщо строкове дане містить число то перетворюємо це строкове дане в число 
      нечислові значення Tavg    замінюємо на  (Tmax + Tmin)/2;
      нечислові начення WetBulb  замінюємо на   на DewPoint + середнє значення різниці
      між  WetBulb і DewPoint = WB_DPt;


Результат підготовки записаний в  cls_weather_prepare.csv та cls_train_prepare.csv
'''
# Відбір даних train.csv
dt = pd.read_csv('D:\Project\\train.csv')
data_t = dt[['Date','Latitude', 'Longitude', 'NumMosquitos', 'WnvPresent']]
data_t.dtypes.to_excel('D:\Project_classific\\cls_train_types.xlsx')
data_t.to_csv('D:\Project_classific\\cls_train_prepare.csv')

# відбір даних weather.csv
data_m = pd.read_csv('D:\Project\weather.csv')
data_m.dtypes.to_excel('D:\Project_classific\cls_weather_types.xlsx')


row, col = data_m.shape

# заміна нечислових значень Tavg  на (Tmax + Tmin)/2

name = 'Tavg'
for r in range(row):
    if not (isinstance(data_m.loc[r, name], (int, float))):
        try:
            a = data_m.loc[r, name]
            data_m.loc[r, name] = float(a)
        except:
            data_m.loc[r, name] = (data_m.loc[r, 'Tmax'] + data_m.loc[r, 'Tmin']) / 2
# зміна типу даних на float
data_m['Tavg'] = data_m['Tavg'].astype(float)

#  WetBulb з нечисловим значенням при першому проході по стовпчику замінюємо на 0 а при другому
#  на DewPoint + середнє значення різниці між даними стовпчиків WetBulb і DewPoint = wb_dpt

# перший прохід стовпчика WetBulb

name = 'WetBulb'
for r in range(row):
    if not (isinstance(data_m.loc[r, name], (int, float))):
        try:
            a = data_m.loc[r, name]
            data_m.loc[r, name] = float(a)
        except:
            data_m.loc[r, name] = 0

# другий прохід стовпчика
# середнє значення різниці WetBulb і DewPoint. Рядки з  WetBulb = 0 не враховуються
WB_DPt= data_m[['WetBulb','DewPoint']]
WB_DPt = WB_DPt[WB_DPt['WetBulb'] != 0]
WB_DPt['Subtract'] = WB_DPt['WetBulb'] - WB_DPt['DewPoint']
wb_dpt_avg = WB_DPt['Subtract'].mean()
# заміна нульових значення WetBulb в data_m на DewPoint + wb_dpt_avg

for r  in range(row):
    if(data_m.loc[r,'WetBulb'] == 0):
        data_m.loc[r, 'WetBulb'] = data_m.loc[r,'DewPoint'] + wb_dpt_avg
   # зміна типу даних на float
data_m['WetBulb'] = data_m['WetBulb'].astype(float)
col_n = ['Station', 'Date', 'Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb']

# Заміна нечислових значент на nan
# 	Якщо дане типу str містить число, то перетворюємо  це дане в число типу float.
# В іншому випадку присвоюємо йому значення np.nan.
for name, val in data_m.iteritems ():
    if name not in col_n:

        for r in range(row):
            try:
                data_m.loc[r, name] = float(data_m.loc[r, name])
            except:
                data_m.loc[r, name] = np.nan

# кількість даних з nan по даним
data_nulsum = data_m.isnull().sum()
data_nulsum.to_excel('D:\Project_classific\cls_data_nulsum.xlsx')

# Відбір даних для моделі
data_m = data_m[['Station', 'Date', 'Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb', 'Heat', 'Cool', 'PrecipTotal', \
             'StnPressure', 'SeaLevel','ResultSpeed', 'ResultDir', 'AvgSpeed']]
# замінюємо  значення даних  з nan на середнє значення по стовпчику
nan_name = ['Heat', 'Cool', 'PrecipTotal', 'StnPressure', 'SeaLevel', 'AvgSpeed' ]
for name in nan_name:
    data_m[name].fillna(int(data_m[name].mean()), inplace=True)
    data_m[name] = data_m[name].astype(float)

data_nulsum = data_m.isnull().sum()
# заміна типу даних на float
name_astype = ['Tmax', 'Tmin','DewPoint','ResultDir']
for name in name_astype:
    data_m[name] = data_m[name].astype(float)

data_m.dtypes.to_excel('D:\Project_classific\cls_weather_types_end.xlsx')

data_m.to_csv('D:\Project_classific\cls_weather_prepare.csv', index = False)

