import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np

def openData(id):
    dir = "hs_g73_m08"
    file_name = 'hs_' + str(id) + '_m08_0903_1355.csv'
    file = os.path.join(dir, file_name)
    data = pd.read_csv(file, encoding='euc-kr')
    return data


def exercise(id):
    data = openData(id)
    exerInside = data[data.State == "실내운동하기"]
    exerOutside = data[data.State == "실외운동하기"]
    insideCount = len(exerInside)  #실내운동 총 횟수
    outsideCount = len(exerOutside)  #실외운동 총 횟수
    x = np.arange(2)
    plt.bar(x, [insideCount, outsideCount])
    plt.xticks(x, ["실내운동", "실외운동"])
    plt.ylim(0, max(insideCount,outsideCount) + 5)
    plt.show()

def zValue(id):
    data = openData(id)
    out = data["State"].isin(["외출하기"])
    data = data[~out]
    print(data)
    Zcolumn = data['Z'].value_counts()
    x = np.arange(4)
    plt.bar(x, [Zcolumn["부동"], Zcolumn["미동"], Zcolumn["활동"], Zcolumn["매우 활동"]])
    plt.xticks(x, ["부동", "미동", "활동", "매우 활동"])
    plt.ylim(0, max(Zcolumn["부동"], Zcolumn["미동"], Zcolumn["활동"], Zcolumn["매우 활동"] + 5))
    plt.show()

def goOut(id):
    data = openData(id)
    out = data[data.State == "외출하기"]



# 기록된 날이 며칠인지
def date(id):
    data = openData(id)
    print(data.iloc[1,1][9:11])
    print(len(data))
    dateCount = []
    for i in range (len(data)):
        if((data.iloc[i,1][9:11] not in dateCount)):
            dateCount.append(data.iloc[i,1][9:11])
    print(dateCount) # test
    return len(dateCount)




