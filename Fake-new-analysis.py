# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18GUIvdTITuUcmWGQ7pwEyrPi1ze0JkDa
"""



"""importing the dependencies"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#printing the stopwords in english

print(stopwords.words('english'))

#loading dataset to a pandas data frame
news_dataset= pd.read_csv('/content/train.csv')

news_dataset.shape

news_dataset.head()

#counting the number of missing values in the dataset
news_dataset.isnull().sum()

#replacing the null value with empty string.
news_dataset = news_dataset.fillna('')

news_dataset['content'] = news_dataset['author'] + ' ' + news_dataset['title']

print(news_dataset['content'])

X=news_dataset.drop(columns='label', axis=1)
Y=news_dataset['label']

print(X)
print(Y)

"""stemming"""

#stemming
port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-z A-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

news_dataset['content'] = news_dataset['content'].apply(stemming)

print(news_dataset['content'])

#separating the data and label
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(X)

print(Y)

Y.shape

#converting text data to numerical data
vectorizer = TfidfVectorizer()  # Adjust min_df as needed
vectorizer.fit(X)
X = vectorizer.transform(X)

print(X)

X_train, X_test,Y_train,Y_test= train_test_split(X,Y, test_size=0.2, stratify=Y,random_state=2)

model=LogisticRegression()

#training the model
model.fit(X_train,Y_train)

#accuracy score
X_train_prediction=model.predict(X_train)
training_data_accuracy=accuracy_score(X_train_prediction, Y_train)

print('accuracy score of the training score:', training_data_accuracy)

X_test_prediction=model.predict(X_test)
test_data_accuracy=accuracy_score(X_test_prediction, Y_test)

print('accuracy score of the test score:', test_data_accuracy)

#making a predictive system
X_new=X_test[3]

prediction=model.predict(X_new)
print(prediction)

if(prediction[0]==0):
  print('The news is Real')
else:
  print('The news is Fake')

print(Y_test[3])

