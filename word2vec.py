from gensim.models.word2vec import Word2Vec
import pandas as pd
from bool_text import delete_emoji

filename = 'data/추천키워드/건강/건강코로나'
data = pd.read_csv(filename+'.csv', sep = ",", encoding = "utf-8")

token_result=[]
tags=data['keywords'].to_numpy()

for i in tags:
    token=i.split(',')
    retoken=[]
    for j in token:
        no_emoji = delete_emoji(j)
        if bool(no_emoji) == True:
            retoken.append(no_emoji)
    token_result.append(retoken)

model = Word2Vec(sentences = token_result, size=100,window=5,min_count=10,workers=4,iter=100,sg=1)
#학습 완료시 필요없는 메모리 unload
model.init_sims(replace=True)


from sklearn.manifold import TSNE
import matplotlib as mpl
import matplotlib.pyplot as plt
import gensim
import gensim.models as g
#그래프에서 마이너스 폰트 깨지는 문제 현상에 대한 대처
mpl.rcParams['axes.unicode_minus'] = False

vocab = list(model.wv.vocab)
X = model[vocab]

tsne = TSNE(n_components=2)

X_tsne = tsne.fit_transform(X[:50,:])
df = pd.DataFrame(X_tsne, index=vocab[:50], columns=['x', 'y'])

fig = plt.figure()
plt.rc('font', family='NanumGothic')
fig.set_size_inches(40, 20)
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'], df['y'])

for word, pos in df.iterrows():
    ax.annotate(word, pos, fontsize=30)
plt.show()
plt.savefig(filename+'.png',dpi=300)