import warnings
import pandas as pd
import numpy as np
# Импортирование необходимых модулей и атрибутов

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


warnings.filterwarnings('ignore')

# Загрузка набору даних
data = pd.read_csv('D:\Project_classific\cls_wnv_dubl_mod.csv')
# X - 'Tmax',  'DewPoint',  'Heat',  'PrecipTotal', 'StnPressure',
#                        'ResultSpeed', 'ResultDir','Latitude', 'Longitude'
# y - 'WnvPresent'
# Формуємо масиви даних
X = data.drop(columns = 'WnvPresent').to_numpy()
y = data.loc[:,'WnvPresent'].to_numpy()


# Поділ набору даних на тренувальні ( навчальні) та тестові частини
# test_size показує, який обсяг даних потрібно виділити для тестового набору
# зберігаємо 20% даних для тестування (оцінки) нашого класифікатора а 80% використовуємо для навчання (тренування)
test_size = 0.2
# Random_state —  сид для випадкової генерации
seed = 7
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

# Налаштування параметрів оцінювання алгоритму
# кратність перехресної перевірки на тренувальних даних
num_folds = 4

# кількість дерев у лісі (для алгоритму Random Forest Classifier)
n_estimators = 100

# метрика для підрахунку правильних відповідей
# accuracy – це доля вірно класифікованих наборів даних
scoring = 'accuracy'

# список алгоритмів моделей. Кожному алгоритму (методу моделювання) для зручності присвоєна коротка назва
models = []
# Лінійний алгоритм  - Логістична регресія
models.append(('LR', LogisticRegression()))

# Нелінійні алгоритми
# Метод k-найближчих сусідів (класифікація) / K-Neighbors Classifier (KNN)
models.append(('KNN', KNeighborsClassifier()))
# Дерева прийняття рішень / Decision Tree Classifier (CART)
models.append(('CART', DecisionTreeClassifier()))
# Наївний класифікатор Байєса / Naive Bayes Classifier (NBC)
models.append(('NBC', GaussianNB()))
# Метод опорних векторів (класифікация) / C-Support Vector Classification (SVC)
models.append(('SVC', SVC()))

# Ансамблевий алгоритм Випадковий ліс (класифікація) / Random Forest Classifier (RF)
models.append(('RF', RandomForestClassifier(n_estimators = n_estimators)))


# Оцінювання ефективності виконання кожного алгоритму
scores = []
names = []
results = []
predictions = []
msg_row = []
# Таблиця результатів
col_name = ['Назва методу моделювання', 'Точність', 'Точність KFold',  'Середнє квадратичне відхилення']
res = pd.DataFrame(columns = col_name)
# поточний номер рядка таблиці результатів
row_res = 0
for name, model in models:
     #  Оцінка моделювання методом name з використанням перехресного методу формування навчальної  і тестової виборок KFold
     # kfold - генератор (ітератор)  виборок даних перехресним методом
     # при кожному виклику буде повертати одну з 4-х (num_folds = 4)  виборок
    kfold = KFold(n_splits = num_folds)


    # При перехресній перевірці K-FOLD  вибірка розбивається на num_folds складок (фолдів) з яких  (num_folds-1) складок
    # використовується  для навчання а остання - для тестування
    # Результуюча модель перевіряється на даних, що залишилися.
    #  Цей процес повторюється num_folds разів, і на кожному етапі створюється нова модель методом name для якої
    #  обчислюється показник продуктивності, такий як «ТОЧНІСТЬ»  (scoring = 'accuracy')
    #  cross_val_score - значення показників продуктивности   моделей отриманих на кожному етапі


    cv_results = cross_val_score(model, X, y, cv=kfold, scoring = scoring)

    # список назв використаних методів
    names.append(name)
    # список  показникікв продуктивності
    results.append(cv_results)

# Оцінка моделювання методом name без використання перехресного методу формування виборок KFold

    # підгонка моделі по навчальнй виборці
    m_fit = model.fit(X_train, Y_train)
    # прогнозування по тестовій виборці
    m_predict = model.predict(X_test)
    # список результатів прогнозування для отриманої  моделі
    predictions.append(m_predict)
    # Оцінка моделювання методом name
    m_score = model.score(X_test, Y_test)
    # список оцінок методів моделювання
    scores.append(m_score)
# Результати:
# name - скорочена назва назва методу моделювання,
# cv_results.mean() - середнє значення  метрики 'accuracy', отриманих по цьому методу моделювання
#                     при використанні перехресного методу формування виборок KFold
# cv_results.std() - середнє квадратичне відхилення значення метрики ‘accuracy’ (в скобках).
# m_score - значення  метрики 'accuracy', отримане по цьому методу моделювання
#           без використання перехресного методу формування виборок KFold

# Занесення результатів в таблицю

    res.loc[row_res,'Назва методу моделювання'] = name
    res.loc[row_res,'Точність'] = m_score
    res.loc[row_res,'Точність KFold'] = cv_results.mean()
    res.loc[row_res,'Середнє квадратичне відхилення'] = cv_results.std()

    res.to_excel('D:\Project_classific\cls_dubl_res.xlsx')
    res.to_csv('D:\Project_classific\cls_dubl_res.csv', index=False)

    row_res += 1



