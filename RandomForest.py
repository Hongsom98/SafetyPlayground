from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def Predict():
    rf_model = RandomForestClassifier(n_estimators=500, max_depth=25, max_features='auto', bootstrap=False, class_weight='balanced_subsample')

    data = pd.read_csv('2021_dummie.csv', encoding='ms949')
    x = data[['HorseNum', 'Age', 'Weight', 'HorseWeight', 'Top1Win', 'Top2Win', 'Distance', 'S1F', 'Cornor3', 'G3F', 'Cornor4',
              'HorseWin', 'HorseRankInTop2', 'HorseRankInTop3', 'Cutted', 'Male', 'Female', 'Good', 'Rain', 'Fog']]
    y = data[["HorseWin", "HorseRankInTop2", "HorseRankInTop3"]]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    rf_model.fit(X_train, y_train['HorseWin'])
    rf_Win = rf_model.predict(X_test)
    rf_model.fit(X_train, y_train['HorseRankInTop2'])
    rf_Top2 = rf_model.predict(X_test)
    rf_model.fit(X_train, y_train['HorseRankInTop3'])
    rf_Top3 = rf_model.predict(X_test)

    d = pd.DataFrame()
    d['HorseWin'] = rf_Win
    d['HorseRankInTop2'] = rf_Top2
    d['HorseRankInTop3'] = rf_Top3

    temp = []
    for i in X_test['Age']:
        temp.append(i)
    d['Age'] = temp

    temp = []
    for i in X_test['Cutted']:
        temp.append(i)
    d['Cutted'] = temp

    temp = []
    for i in X_test['Male']:
        temp.append(i)
    d['Male'] = temp

    temp = []
    for i in X_test['Female']:
        temp.append(i)
    d['Female'] = temp

    temp = []
    for i in X_test['HorseNum']:
        temp.append(i)
    d["HorseNum"] = temp


    PredictList = []

    for i in range(len(d)):
        temp = list(d.loc[i])
        if temp[4]:
            temp.append("C")
        elif temp[5]:
            temp.append("M")
        elif temp[6]:
            temp.append("F")
        del temp[4:7]
        PredictList.append(temp)

    with open('PredictSet.txt', 'w') as f:
        for item in PredictList:
            for i in item:
                f.write(str(i)+" ")
            f.write('\n')

Predict()
