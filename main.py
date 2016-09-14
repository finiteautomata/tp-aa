# -*- coding: utf-8 -*-
u"""Script para árboles."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.grid_search import GridSearchCV
from dataframe_builder import DataFrameBuilder
# Ignorar Warning de sklearn (no es importante)
import warnings
warnings.filterwarnings('ignore',
                        message='Changing the shape of non-C contiguous array')

print "Reading files..."
ham_txt = json.load(open('data/ham_dev.json'))
spam_txt = json.load(open('data/spam_dev.json'))

print "Done."

builder = DataFrameBuilder(ham=ham_txt, spam=spam_txt)
df = builder.build()

"""
Algunas observaciones previas:

El árbol que se genera no es usando ID3 sino CART. Una pequeña introducción
se puede ver en

http://scikit-learn.org/stable/modules/tree.html#tree-algorithms-id3-c4-5-c5-0-and-cart

No está muy completo el asunto ahí, habría que hurgar algún paper extra

Opciones:

- criterion: gini o entropy. Son dos medidas distintas
- splitter: No estoy muy seguro
- max_depth: máxima profundidad del árbol
- max_features: qué porcentaje de variables tomo a la hora de partir un nodo.
  Estas variables se eligen aleatoriamente
- min_samples_split: cuántos elementos tengo que tener en un nodo para decidir
  partirlo
"""

options = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': range(2, 52, 5),
    'max_features': np.arange(0.1, 1.0, 0.1),
    'min_samples_split': range(2, 102, 5),
}

# Preparo data para clasificar
X = df[builder.list_of_attributes].values
y = df['class'] == 'spam'

for scoring in ['precision', 'accuracy', 'f1']:
    clf = DecisionTreeClassifier()

    print("=" * 80 + "\n")
    print("Scoring {}".format(scoring))

    grid_search = GridSearchCV(
        clf, scoring=scoring, param_grid=options, n_jobs=4)
    grid_search.fit(X, y)

    print "Mejor combinación: {}".format(grid_search.best_params_)
    print "Mejor valor: {}".format(grid_search.best_score_)
