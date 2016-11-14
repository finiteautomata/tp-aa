"""Entrypoint de transformers."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_union
from sklearn_pandas import DataFrameMapper
from .base import BaseTransformer
from .payload import SpaceTransformer, LenTransformer, AddWordsTransformer

options = {
    'max_features': 100,
    'ngram_range': (1, 1),
    'min_df': 0.001,
    'max_df': 0.75,
}


payload_transformer = make_union(
    SpaceTransformer(),
    LenTransformer(),
    AddWordsTransformer(),
    TfidfVectorizer(**options),
)

transformer = DataFrameMapper([
    ('payload', payload_transformer)
])