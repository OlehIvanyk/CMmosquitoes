import  pandas as pd
import warnings
from sklearn.model_selection import train_test_split
# Имплементація нейроної мережі
from sklearn.neural_network import MLPClassifier
warnings.filterwarnings('ignore')

# Прогноз зараження комарів  вірусом з використанням нейромережі


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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Ініціалізація нейронної мережі

neuralnet = MLPClassifier(solver='lbfgs', alpha=4.0)
neuralnet.fit(X_train, y_train) # навчання мережі
accuracy = neuralnet.score(X_test, y_test) # Точність роботи мережі

print(str(accuracy * 100) + "% accuracy") #

# m_predict - масив з результатами прогнозу
m_predict = neuralnet.predict(X_pred)
print(m_predict)
row, col = res_tab.shape

for n in range(row):

    if (m_predict[n] == 1):
        res_tab.loc[n,'Зараження комара вірусом є?'] = 'Так'
    else:
        res_tab.loc[n, 'Зараження комара вірусом є?'] = 'Ні'

res_tab.to_excel('D:\Data\cls_res_neuro.xlsx')