# -*- coding: utf-8 -*-
"""Clase que se encarga de construir el dataframe en base a los ham y spam."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import numpy as np
import pandas as pd
import json
import config


def load_dev_data(**kwargs):
    """Carga el dataframe de dev."""
    builder = DataBuilder()

    return builder.build()


def load_small_dev_data(**kwargs):
    """Carga datos de desarrollo 'de prueba'."""
    builder = DataBuilder()

    return builder.build(
        spam_path=config.spam_small_dev_path,
        ham_path=config.ham_small_dev_path
    )


def load_test_data(**kwargs):
    """Carga el dataframe de test."""
    builder = DataBuilder()

    return builder.build(
        spam_path=config.spam_test_path,
        ham_path=config.ham_test_path
    )


class DataBuilder(object):
    """
    Construye un dataframe en base al dataset de spam y ham.

    Uso:

    > ham_path = 'data/ham_dev.json')
    > spam_path = 'data/spam_dev.json')
    > builder = DataFrameBuilder()
    > df = builder.build(spam_path=spam, ham_path=ham_path)
    """

    def build(self,
              spam_path=config.spam_dev_path, ham_path=config.ham_dev_path):
        u"""Construye el dataframe desde 0."""
        spam = json.load(open(spam_path))
        ham = json.load(open(ham_path))

        u"""Construye el dataframe con todos los datos."""

        klass = [True] * len(spam) + [False] * len(ham)

        return pd.DataFrame({'text': spam + ham}), np.array(klass)
