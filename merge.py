import pandas as pd
import os

fileDir = r"data/추천키워드/취미생활"
fileExt = r".txt"
file_list=[os.path.join(fileDir, _) for _ in os.listdir(fileDir) if _.endswith(fileExt)]
data = pd.DataFrame()

for filename in file_list:
    df = pd.read_csv(filename, sep = ",", encoding = "utf-8")
    data = pd.concat([data,df])
token_result=[]
tags=data.fillna(0).loc[:,'2':].to_numpy()
for i in tags:
    token=[]
    for j in i:
        if type(j)==str:
            token.append(j)
    token_result.append(token)
#빈값 리스트에서 제거
token_result = [v for v in token_result if v]
#
token_list = [','.join(i) for i in token_result]
data = pd.DataFrame(token_list,columns=['keywords'])
data.drop_duplicates(inplace=True)
data.to_csv(fileDir+'코로나.csv')
