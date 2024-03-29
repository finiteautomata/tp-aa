"""Entrypoint de transformers."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_union
from sklearn_pandas import DataFrameMapper
from base import BaseTransformer
from .payload import SpaceTransformer, LenTransformer, AddWordsTransformer
from .header import ContentTypeTransformer, ParticipantsTransformer, DateTransformer

options = {
    'max_features': 200,
    'ngram_range': (1, 2),
    'min_df': 0.001,
    'max_df': 0.75,
}


payload_transformer = make_union(
    SpaceTransformer(),
    LenTransformer(),
    AddWordsTransformer(),
    TfidfVectorizer(**options),
)

parsed_mail_transformer = make_union(
    ContentTypeTransformer(),
    ParticipantsTransformer(),
    DateTransformer(),
)


def MyTransformer():
    return DataFrameMapper([
        ('payload', payload_transformer),
        ('parsed_emails', parsed_mail_transformer),
    ])

transformer = MyTransformer()
