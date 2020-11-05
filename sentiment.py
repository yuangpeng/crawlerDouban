from langconv import *


def traditional2simplified(text):
    text = Converter('zh-hans').convert(text)
    return text


dataset["CONTENT"] = dataset.CONTENT.apply(lambda x: traditional2simplified(x))

import jieba
from sklearn.feature_extraction.text import CountVectorizer


def get_stopwords():
    stopwords = [line.strip() for line in open('data/stopwords/stopword_normal.txt', encoding='UTF-8').readlines()]
    return stopwords


import re

stopwords = get_stopwords()


def text_process(text):
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", "", text)

    ltext = jieba.lcut(text)
    res_text = []
    for word in ltext:
        if word not in stopwords:
            res_text.append(word)
    return res_text


X = dataset.CONTENT
y = dataset.label
bow_transformer = CountVectorizer(analyzer=text_process).fit(X)
X = bow_transformer.transform(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=99)

from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB()
nb.fit(X_train, y_train)
preds = nb.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report

print(classification_report(y_test, preds))


def sentiment_pred(text):
    text_transformed = bow_transformer.transform([text])
    score = nb.predict(text_transformed)[0]
    return score
