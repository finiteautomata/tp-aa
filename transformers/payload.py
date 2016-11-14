#! coding: utf-8
"""Transformers que se aplican sobre el payload."""

import numpy as np
from . import BaseTransformer


class LenTransformer(BaseTransformer):
    """Clase que agrega len al coso este."""

    def transform(self, data):
        u"""Aplica la transformación."""
        return np.array([len(t) for t in data]).reshape(-1, 1)


class SpaceTransformer(BaseTransformer):
    """Clase que agrega len al coso este."""

    def transform(self, data):
        u"""Aplica la transformación."""
        return np.array([t.count(" ") for t in data]).reshape(-1, 1)


class AddWordsTransformer(BaseTransformer):
    """Agrega counts de varias palabras."""

    def transform(self, data):
        u"""Aplica la transformación."""
        words = [
            "dear", "friend", "hello""$", "earn", "investment", "profit",
            "profits", "credit", "opportunity", "income", "cost" "promotion",
            "why pay more?", "click", "add",
            "meet singles", "viagra", "sex", "penis", "vagina", "pussy",
            "fuck", "girl", "erect", "enlargement"
            "free", "cc:", "gif", "help", "photo", "video", "http", "dollar",
            "million", "|", "nigeria", "million", "password", "of", "bill",
            "it's time", "sale", "hi", "-->", "weight", "lose",
            "administrator", "order", "clearance", "meet singles"
        ]

        new_columns = []

        for word in words:
            new_columns.append([t.lower().count(word) for t in data])

        ret = np.array(new_columns)

        return ret.transpose()
