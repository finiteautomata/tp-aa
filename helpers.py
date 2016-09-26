#! coding: utf-8
"""Auxiliares varios."""

import pandas as pd
import config
from sklearn.metrics import precision_score, accuracy_score, f1_score, recall_score, roc_auc_score
from dataframe_builder import DataFrameBuilder

scores = [
    precision_score,
    accuracy_score,
    f1_score,
    recall_score,
    roc_auc_score
]


def get_scores(classifier):
    """Calcula scores para el clasificador usando datos de test."""
    builder = DataFrameBuilder(dataframe_path=config.test_dataframe_path)
    df_test = builder.build(
        spam_path=config.spam_test_path,
        ham_path=config.ham_test_path)

    X_test = df_test.design_matrix
    Y_test = df_test.outcomes

    print X_test.shape

    results = pd.DataFrame(index=[classifier.__class__.__name__])
    for other_scorer in scores:
        Y_pred = classifier.predict(X_test)

        results[other_scorer.func_name] = [other_scorer(Y_test, Y_pred)]
    return results
