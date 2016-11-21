#! coding: utf-8
"""Auxiliares varios."""

from sklearn.metrics import precision_score, accuracy_score, f1_score, recall_score, roc_auc_score
import pandas as pd
from data_builder import load_test_data

scores = [
    precision_score,
    accuracy_score,
    f1_score,
    recall_score,
    roc_auc_score
]


def add_prefix(d, prefix):
    u"""
    Devuelve nuevo diccionario cuyas claves son las anteriores más `prefix` como prefijo.

    add_prefix({'k1: 1, 'k2': 2}, 'p__')
    > {'p__k1: 1, 'p__k2': 2}
    """
    return dict((prefix + k, v) for (k, v) in d.iteritems())


def get_scores(classifier, extractor):
    """Calcula scores para el clasificador usando datos de test."""
    df, target = load_test_data()

    x_test = extractor.transform(df)
    y_test = target

    results = pd.DataFrame(index=[classifier.__class__.__name__])
    for other_scorer in scores:
        y_pred = classifier.predict(x_test)

        results[other_scorer.func_name] = [other_scorer(y_test, y_pred)]
    return results
