import pandas as pd

owner_id = int(input("Enter owner_id: "))
if owner_id >= 30064:
    data = pd.read_csv("hs_g73_m08/hs_" + str(owner_id) + "_m08_0903_1356.csv", encoding='cp949' ,index_col=0)    
else:
    data = pd.read_csv("hs_g73_m08/hs_" + str(owner_id) + "_m08_0903_1355.csv", encoding='cp949' ,index_col=0)

time = data["Time"]
state = data["State"]
