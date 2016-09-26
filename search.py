#! coding: utf-8
u"""Auxiliares para búsqueda de hiperparámetros."""

from sklearn.grid_search import RandomizedSearchCV


def find_best_classifier(df, clf_class,
                         search_class=RandomizedSearchCV, **kwargs):
    """Busca el mejor clasificador usando grid o randomized search."""
    # Preparo data para clasificar
    X = df.design_matrix
    y = df.outcomes

    classifier = clf_class()

    print "Buscando parámetros para {}".format(classifier.__class__.__name__)

    search = search_class(classifier, **kwargs)
    search.fit(X, y)

    print "Mejor combinación: {}".format(search.best_params_)
    print "Mejor valor: {}\n\n".format(search.best_score_)

    return search.best_estimator_
