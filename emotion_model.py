from keras.models import Sequential, load_model
from keras.layers import Dense,LSTM,Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.utils import np_utils
from keras.callbacks import EarlyStopping,ModelCheckpoint
from collections import Counter

import os
import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# seed 값 설정
seed = 0
np.random.seed(seed)
tf.random.set_seed(3)

#train, test 데이터
train_data = pd.read_csv("data/감정분석/감정분석코로나_train_set.csv")
test_data = pd.read_csv("data/감정분석/감정분석코로나_test_set.csv")

X_train = [i.split(',') for i in train_data['keywords']]
X_test = [i.split(',') for i in test_data['keywords']]
y_train = np_utils.to_categorical(train_data['label'])

from keras.preprocessing.text import Tokenizer
max_words = 35000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

max_len = 20
X_train = pad_sequences(X_train,maxlen=max_len)
X_test = pad_sequences(X_test,maxlen=max_len)

model = Sequential()
model.add(Embedding(max_words,100))
model.add(LSTM(128,activation='tanh'))
model.add(Dense(2,activation='softmax'))

model_save_folder_path = './model/'
if not os.path.exists(model_save_folder_path):
    os.mkdir(model_save_folder_path)
model_path = model_save_folder_path + 'best_model.h5'

es = EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=10)
mc = ModelCheckpoint(filepath=model_path, monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train,y_train,epochs=50,batch_size=10,validation_split=0.2,callbacks=[es,mc])

loaded_model = load_model('model/best_model.h5')
predict = loaded_model.predict(X_test)
predict_labels = np.argmax(predict,axis=1)

#예측값들 넣어주기
test_data['values'] = predict_labels
test_data.groupby('values').size().plot.pie(explode=[0.0,0.1],autopct='%1.2f%%',labels=['neg','pos'],shadow=True,textprops={'fontsize': 14})
plt.ylabel("")
plt.title('Pie Chart of Corona19', fontsize=20)
plt.show()
plt.savefig("data/감정분석/감정분석코로나_pie_chart.png")
