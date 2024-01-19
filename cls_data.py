import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Створення робочого фрейму  даних data_pr
#
# Спочатку   В data_pr копіюються  стовпчики Date, Latitude, Longitude,  NumMosquitos,  WnvPresent  з cls_train_prepare.csv.
#
# Одній і тій же даті в data_pr відповідає певна кількість рядків з координатами пастки і даними NumMosquitos та WnvPresent.
# Потрібно визначити для  кожного такого рядка метеодані  на зазначену в них дату
# Добавляємо в data_pr нові стовпчики для метеоданих
#  Копіюємо з W_weather_prepare.csv метеодані  в  фрейм weather.
#  В фреймі weather метеодані по кожній даті задані для  двох метеостанцій Station1 та Station2.
# Для  кожного вибраного  рядка фрейму data_pr беремо дату Date з цього рядка  і по ній в фреймі weather отримуємо метеодані
# по одній з двох  метеостанцій. А саме вибираємо метеодані з тієї метеостанції яка знаходиться найближе до місця розташування
# пастки, координати якої є в вибраному рядку фрейму data_pr.

# Заповнений фрейм data_pr містить наступні дані:
# 'Date','NumMosquitos', 'Wnvpresent', 'Latitude', 'Longitude', 'Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb', 'Heat',
# 'Cool',  'PrecipTotal', 'StnPressure', 'ResultSpeed', 'ResultDir', 'AvgSpeed','SeaLevel'




def distance(adr):
    # Вибір найближчої метеостанції Station1 або Station2 від заданої геокординатами adr = (Довгота, Широта)
    # місцеположення пастки


    #  геокоординати (Lat, Lon) метеостанцій Station1 або Station2 з DSprojekt1/StationsLocation.txt
    st1 = (41.995, -87.933)
    st2 = (41.786, -87.752)

    # Вибір найближчої станціЇ: 1 - Station1, 2 - Station2
    if geodesic(st1, adr).meters < geodesic(st2, adr).meters:
        return 1
    else:
        return 2





data_pr = pd.read_csv('D:\Project_classific\cls_train_prepare.csv')


# Добавляємо стовпчики в data_pr

col_w = [ 'Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb', 'Heat', 'Cool',  'PrecipTotal', \
         'StnPressure', 'ResultSpeed', 'ResultDir', 'AvgSpeed', 'SeaLevel']

data_pr[col_w] = 0



# Таблиця метеоданих,
weath = pd.read_csv('D:\Project_classific\cls_weather_prepare.csv')



# Заповнюємо стовпчики 'Tmax', 'Tmin', 'Tavg',  'WetBulb','DevPoint', 'Heat', 'Cool',  'PrecipTotal',
#  'StnPressure', 'ResultSpeed', 'ResultDir', 'AvgSpeed', 'SeaLevel' data_pr даними з фрейму weath для
#  найближчої метеостанції

# перебираємо рядки робочої таблиці
for rowindex, row in data_pr.iterrows():
    # вибираємо координати пастки для комарів з поточного рядка data_pr
    adress = (row['Latitude'], row['Longitude'])
    #  Знаходимо індекс найближчої до пастки метеостанції
    st = distance(adress)
    #  По даті з поточного рядка data_pr Копіюємо з weather в w_rows   рядки
    #   з метеоданними (2 рядка з метеоданими з Station1 та Station2 )
    w_rows = weath[weath['Date'] == row['Date']]
    #  station_w_row містить тільки метеоданні від найближчої метеостанції
    station_w_row = w_rows[w_rows['Station'] == st]
    # Копіюємо метеодані  з st_w_row в data_pr
    idx = station_w_row.index
    for col in col_w:
        data_pr.loc[rowindex, col] = station_w_row.at[idx[0], col]

# імпорт таблиці даних в CSV-файл
data_pr.to_csv('D:\Project_classific\cls_dubl_data.csv', index=False)

# Видаляємо дублікати рядків

data_pr = data_pr.drop_duplicates(subset=['WnvPresent', 'Tmax', 'Tmin', 'Tavg', 'DewPoint', 'WetBulb', 'Heat', 'Cool',
                                          'PrecipTotal', 'StnPressure', 'ResultSpeed', 'ResultDir', 'AvgSpeed',
                                          'SeaLevel'])
# імпорт даних без дублікатів рядків в CSV-файл
data_pr.to_csv('D:\Project_classific\cls_data.csv', index=False)
