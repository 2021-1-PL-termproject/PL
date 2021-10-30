import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np

def openData(id):
    if(id <= 30063):
        dir = "hs_g73_m08"
        file_name = 'hs_' + str(id) + '_m08_0903_1355.csv'
    else:
        dir = "hs_g73_m08"
        file_name = 'hs_' + str(id) + '_m08_0903_1356.csv'
    file = os.path.join(dir, file_name)
    data = pd.read_csv(file, encoding='cp949')
    return data

def openID():
    data = pd.read_excel("user_profile.xlsx", engine ='openpyxl')
    return data

#한달 전체에 대한 운동 총 횟수
def exercise(id):
    data = openData(id)
    exerInside = data[data.State == "실내운동하기"]
    exerOutside = data[data.State == "실외운동하기"]
    insideCount = len(exerInside)  #실내운동 총 횟수
    outsideCount = len(exerOutside)  #실외운동 총 횟수

    return [insideCount, outsideCount]

# date는 date 함수를 통한 운동 일수
def exerciseMean(id):
    if (date(id) == "no Data"):
        return 0
    else:
        X = exercise(id)[0] + exercise(id)[1]
        return round(int(X) / date(id), 2)

#사용자 전체 하루 평균 운동 횟수
def exerciseAll():
    data = openID()
    x = 0.0
    for i in range(len(data)):
        x += exerciseMean(data.iloc[i]["id"])
    return x / len(data)

# ZValue 횟수
def zValue(id):
    data = openData(id)
    out = data["State"].isin(["외출하기"])
    data = data[~out]
    Zcolumn = data['Z'].value_counts()
    x = np.arange(4)
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.bar(x, [Zcolumn["부동"], Zcolumn["미동"], Zcolumn["활동"], Zcolumn["매우 활동"]])
    plt.xticks(x, ["부동", "미동", "활동", "매우 활동"])
    plt.ylim(0, max(Zcolumn["부동"], Zcolumn["미동"], Zcolumn["활동"], Zcolumn["매우 활동"] ) + 5)


#Zvalue 점수화
def zValueScore(id):
    data = openData(id)
    out = data["State"].isin(["외출하기"])
    data = data[~out]
    Zcolumn = data['Z'].value_counts()
    X = Zcolumn["부동"] * 0 + Zcolumn["미동"] * 1 + Zcolumn["활동"] * 2 + Zcolumn["매우 활동"] * 3
    return X

#단순 외출 횟수
def goOut(id):
    data = openData(id)
    out = data[data.State == "외출하기"]
    TotalOut = len(out)
    return TotalOut

#사용자의 하루 평균 외출 횟수
def goOutMean(id):
    if (date(id) == "no Data"):
        return 0
    else:
        X = goOut(id)
        return round(int(X) / date(id), 2)

# 전체 사용자 하루 평균 외출 횟수
def goOutAll():
    data = openID()
    x = 0.0
    for i in range(len(data)):
        x += goOutMean(data.iloc[i]["id"])
    return x / len(data)



# 전체와 사용자의 비교 후 메시지
def goOutMsg(id):
    all = goOutAll()
    target = goOutMean(id)
    if(target < 0.7 * all):
        return "하루 평균 외출 횟수가 전체 사용자의 평균에 비해 적어요."
    elif (target < 1.5 * all):
        return "하루 평균 외출 횟수가 전체 사용자 평균과 비슷해요."
    else:
        return "하루 평균 외출 횟수가 전체 사용자 평균보다 높아요! "

# 기록된 날의 수 계산
def date(id):
    data = openData(id)
    if (len(data) == 0):
        return "no Data"
    dateCount = []
    for i in range (len(data)):
        if((data.iloc[i,1][9:11] not in dateCount)):
            dateCount.append(data.iloc[i,1][9:11])
    return len(dateCount)




