#!/usr/bin/env python
# -*- coding: utf-8 -*-
# QingTao

import time
from trace import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import cross_validation
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split

from ClassifyModule.Tools.lood_words import load_words
from ClassifyModule.model.model_path import get_model_path
from sklearn.externals import joblib

'''
使用sklearn 进行分类
'''

train_data, train_labels = load_words()

X_train, X_test, y_train, y_test = train_test_split(train_data, train_labels)

# Create feature vectors
vectorizer = TfidfVectorizer(min_df=5,
                             max_df=0.8,
                             sublinear_tf=True,
                             use_idf=True,
                             decode_error='ignore'
                             )

X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)
joblib.dump(vectorizer, get_model_path('vectorizer'))

# Perform classification with SVM, kernel=linear
classifier_liblinear = svm.LinearSVC()
t0 = time.time()
classifier_liblinear.fit(X_train_vectors, y_train)
t1 = time.time()
prediction_liblinear = classifier_liblinear.predict(X_test_vectors)
t2 = time.time()
time_liblinear_train = t1 - t0
time_liblinear_predict = t2 - t1
# pickle.dump(classifier_liblinear, open(get_model_path('linearSVC'), 'wb'))
joblib.dump(classifier_liblinear, get_model_path('linearSVC'))

# kfold = cross_validation.KFold(len(x1), n_folds=10)

# Perform classification with SVM, kernel=rbf
# classifier_rbf = svm.SVC()
classifier_rbf = svm.SVC(gamma=0.001, C=100.)
t0 = time.time()
classifier_rbf.fit(X_train_vectors, y_train)
t1 = time.time()
prediction_rbf = classifier_rbf.predict(X_test_vectors)
t2 = time.time()
time_rbf_train = t1 - t0
time_rbf_predict = t2 - t1
# pickle.dump(classifier_rbf, open(get_model_path('svc'), 'w'))
joblib.dump(classifier_rbf, get_model_path('svc'))

lr = LogisticRegression(penalty='l1', tol=0.01)
t0 = time.time()
lr.fit(X_train_vectors, y_train)
t1 = time.time()
prediction_lr = lr.predict(X_test_vectors)
t2 = time.time()
time_lr_train = t1 - t0
time_lr_predict = t2 - t1
# pickle.dump(lr, open(get_model_path('lr'), 'w'))
joblib.dump(lr, get_model_path('lr'))

gnb = MultinomialNB()
t0 = time.time()
gnb.fit(X_train_vectors, y_train)
t1 = time.time()
prediction_gnb = gnb.predict(X_test_vectors)
t2 = time.time()
time_gnb_train = t1 - t0
time_gnb_predict = t2 - t1
# pickle.dump(gnb, open(get_model_path('gnb'), 'w'))
joblib.dump(gnb, get_model_path('gnb'))

# Print results in a nice table
print("Results for SVC(kernel=rbf)")
print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
print(classification_report(y_test, prediction_rbf))

print("Results for LinearSVC()")
print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
print(classification_report(y_test, prediction_liblinear))

print("Results for lr")
print("Training time: %fs; Prediction time: %fs" % (time_lr_train, time_lr_predict))
print(classification_report(y_test, prediction_lr))

print("Results for gnb")
print("Training time: %fs; Prediction time: %fs" % (time_gnb_train, time_gnb_predict))
print(classification_report(y_test, prediction_gnb))
