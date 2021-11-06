import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np


def openData(id):
    id = int(id)
    if(id <= 30063):
        dir = "hs_g73_m08"
        file_name = 'hs_' + str(id) + '_m08_0903_1355.csv'
    else:
        dir = "hs_g73_m08"
        file_name = 'hs_' + str(id) + '_m08_0903_1356.csv'
    file = os.path.join(dir, file_name)
    if os.path.isfile(file):
        data = pd.read_csv(file, encoding='cp949')
        return data
    else:
        return 'No user'


def openID():
    data = pd.read_excel("hs_g73_m08/user_profile.xlsx", engine ='openpyxl')
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

def exerciseMent(id):
    if(exerciseMean(id) < exerciseAll() * 0.7):
        return "다른 사용자들에 비해 운동량이 적어요. \n 다음달에는 건강을 위해 주기적인 운동계획을 세워보는게 어떨까요?\n건강을 위해서 운동은 필수!"
    elif(exerciseMean(id) < exerciseAll() * 1.3):
        return "운동을 적절하게 하고 계시네요!. 적절한 운동은 건강을 위해 아주 좋아요. 앞으로도 꾸준히 해주세요!"
    else:
        return "운동량이 다른 사용자들에 비해 많아요. 너무 무리한 운동이 되지 않게 주의하면 좋을 것 같아요!"

# ZValue 횟수
def zValue(id):
    data = openData(id)
    out = data["State"].isin(["외출하기"])
    data = data[~out]
    Zcolumn = data['Z'].value_counts()
    x = np.arange(4)
    zcolumn = Zcolumn.rename_axis('AA').reset_index(name='counts')
    if ((zcolumn['AA'] == "부동").any()):
        A = Zcolumn["부동"]
    else:
        A = 0
    if ((zcolumn['AA'] == "미동").any()):
        B = Zcolumn["미동"]
    else:
        B = 0
    if ((zcolumn['AA'] == "활동").any()):
        C = Zcolumn["활동"]
    else:
        C = 0
    if ((zcolumn['AA'] == "매우 활동").any()):
        D = Zcolumn["매우 활동"]
    else:
        D = 0

    return [A, B, C, D]


#Zvalue 점수화
def zValueScore(id):
    data = openData(id)
    out = data["State"].isin(["외출하기"])
    data = data[~out]
    Zcolumn = data['Z'].value_counts()
    zcolumn = Zcolumn.rename_axis('AA').reset_index(name='counts')
    if ((zcolumn['AA'] == "부동").any()):
        A = Zcolumn["부동"]
    else:
        A = 0
    if ((zcolumn['AA'] == "미동").any()):
        B = Zcolumn["미동"]
    else:
        B = 0
    if ((zcolumn['AA'] == "활동").any()):
        C = Zcolumn["활동"]
    else:
        C = 0
    if ((zcolumn['AA'] == "매우 활동").any()):
        D = Zcolumn["매우 활동"]
    else:
        D = 0
    X = A * 0 + B * 1 + C * 2 + D * 3
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
