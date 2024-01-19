import warnings

import pandas as pd
import numpy as np
# Импортирование необходимых модулей и атрибутов
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from matplotlib import pyplot

warnings.filterwarnings('ignore')


# Загрузка набору метеоданих для якого треба встановити чи будуть заражені комарі чи ні
data = pd.read_excel('D:\Data\data.xlsx')
# Таблиця з результатами
res_tab = data.copy()

X_pred = data.to_numpy()

# Загрузка набору даних для навчання
data = pd.read_csv('D:\Project_classific\cls_wnv_mod.csv')
# X - 'Tmax',  'DewPoint',  'Heat',  'PrecipTotal', 'StnPressure',
#                        'ResultSpeed', 'ResultDir','Latitude', 'Longitude'
# y - 'WnvPresent'
# Формуємо масиви даних
X = data.drop(columns = 'WnvPresent').to_numpy()
y = data.loc[:,'WnvPresent'].to_numpy()


# Стандартизація

pipelines = []

pipelines.append(('SVC', Pipeline([('Scaler', StandardScaler()), ('SVC', SVC())])))



for name, model in pipelines:

    # підгонка моделі по навчальнй виборці
    m_fit = model.fit(X, y)
    # прогнозування по набоу метеоданих
    m_predict = model.predict(X_pred)
# m_predict - масив з результатами прогнозу
row, col = res_tab.shape

for n in range(row):

    if (m_predict[n] == 1):
        res_tab.loc[n,'Зараження комара вірусом є?'] = 'Так'
    else:
        res_tab.loc[n, 'Зараження комара вірусом є?'] = 'Ні'

res_tab.to_excel('D:\Data\cls_res_tab.xlsx')

