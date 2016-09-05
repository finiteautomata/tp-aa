# -*- coding: utf-8 -*-
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import json

from dataframe_builder import DataFrameBuilder

import numpy as np

from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeClassifier


ham_txt = json.load(open('data/ham_dev.json'))
spam_txt = json.load(open('data/spam_dev.json'))

builder = DataFrameBuilder(ham=ham_txt, spam=spam_txt)

df = builder.build()

# Preparo data para clasificar
X = df[builder.list_of_attributes].values
y = df['class']

# Elijo mi clasificador.
clfWithEntropy = DecisionTreeClassifier(criterion="entropy")
clfWithGini = DecisionTreeClassifier(criterion="gini")

# Ejecuto el clasificador entrenando con un esquema de cross validation
# de 10 folds.
resWithEntropy = cross_val_score(clfWithEntropy, X, y, cv=10)
resWithGini = cross_val_score(clfWithGini, X, y, cv=10)

print "Entropy :", np.mean(resWithEntropy), np.std(resWithEntropy)
print "Gini :", np.mean(resWithGini), np.std(resWithGini)
