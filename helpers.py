#! coding: utf-8
"""Auxiliares varios."""

from sklearn.metrics import precision_score, accuracy_score, f1_score, recall_score, roc_auc_score
import pandas as pd
from transformers import extractor
from data_builder import load_test_data

scores = [
    precision_score,
    accuracy_score,
    f1_score,
    recall_score,
    roc_auc_score
]


def get_scores(classifier):
    """Calcula scores para el clasificador usando datos de test."""
    df, target = load_test_data()

    extractor.fit(df)
    extractor.transform(df)
    x_test = df._get_numeric_data().values
    y_test = target

    results = pd.DataFrame(index=[classifier.__class__.__name__])
    for other_scorer in scores:
        y_pred = classifier.predict(x_test)

        results[other_scorer.func_name] = [other_scorer(y_test, y_pred)]
    return results
