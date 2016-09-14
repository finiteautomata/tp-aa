# -*- coding: utf-8 -*-
u"""Script para árboles."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import json
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

options = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': range(2, 10),
}

# Preparo data para clasificar
X = df[builder.list_of_attributes].values
y = df['class'] == 'spam'

for scoring in ['accuracy', 'precision']:
    clf = DecisionTreeClassifier()

    print("=" * 80 + "\n")
    print("Scoring {}".format(scoring))

    grid_search = GridSearchCV(
        clf, scoring=scoring, param_grid=options, n_jobs=4)
    grid_search.fit(X, y)

    print "Mejor combinación: {}".format(grid_search.best_params_)
    print "Mejor valor: {}".format(grid_search.best_score_)
