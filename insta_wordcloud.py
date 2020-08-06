import pandas as pd
from collections import Counter
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

filename = 'data/추천키워드/취미생활/취미생활코로나'
data = pd.read_csv(filename+'.csv', sep = ",", encoding = "utf-8")
result=[]
for i in data['keywords']:
    for j in i.split(','):
        result.append(j)
count_result = Counter(result)
data = pd.DataFrame(count_result.items(),columns=['keyword','values'])
data.sort_values(by=['values'],ascending=False,inplace=True)
data.to_csv(filename+'해시태그순위'+'.csv')

def displayWordCloud(data = None, backgroundcolor = 'white', width=800, height=600 ):
    wordcloud = WordCloud(font_path='/font/NanumGothic.ttf',stopwords = STOPWORDS,
                          background_color = backgroundcolor,
                         width = width, height = height).generate_from_frequencies(data)
    fig=plt.figure(figsize = (30 , 20))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    fig.savefig(filename+'워드클라우드'+'.png')

displayWordCloud(dict(data.to_numpy()))
