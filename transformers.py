#! coding: utf-8
"""Transformers que van agregando los datos al dataframe."""
import email
import re
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion, Pipeline


class BaseTransformer(BaseEstimator, TransformerMixin):
    """Clase base para todos nuestros transformers."""

    def fit(self, x, y=None):
        u"""Este método no hace nada, pero debe estar."""
        return self


class LenTransformer(BaseTransformer):
    """Clase que agrega len al dataframe."""

    def transform(self, data_dict):
        u"""Aplica la transformación."""
        data_dict['len'] = data_dict['text'].apply(lambda t: len(t))

        return data_dict


class SpaceTransformer(BaseTransformer):
    """Clase que agrega len al coso este."""

    def transform(self, data_dict):
        u"""Aplica la transformación."""
        data_dict['spaces'] = data_dict['text'].apply(
            lambda t: t.count(' ')
        )

        return data_dict


class AddWordsTransformer(BaseTransformer):
    """Agrega counts de varias palabras."""

    def transform(self, df):
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

        for word in words:
            df[word + "_count"] = df['text'].apply(
                lambda t: t.lower().count(word)
            )

        return df


class AddHeaderAttributesTransformer(BaseTransformer):
    """Agrega atributos del header."""

    def transform(self, df):
        u"""Aplico transformación."""
        parser = email.parser.Parser()

        parsed_emails = df['text'].apply(
            lambda t: parser.parsestr(t.encode('utf-8')))

        receivers = parsed_emails.apply(
            lambda p: p.get_all("To") or p.get_all("to") or [])
        sender = parsed_emails.apply(
            lambda p: p.get_all("From") or p.get_all("from") or [])

        def join_mails(t):
            return ";".join(t)

        def is_ascii(s):
            try:
                s.encode('ascii')
                return True
            except UnicodeDecodeError:
                return False

        to_text = receivers.apply(join_mails)
        from_text = df['from'] = sender.apply(join_mails)

        df['number_of_receivers'] = to_text.apply(
            lambda t: len(re.findall(r'<.*>', t))
        )

        df['from_non_ascii'] = from_text.apply(
            lambda from_list: not is_ascii(from_list)
        )

        return df

extractor = FeatureUnion([
    ('len', LenTransformer()),
    ('spaces', SpaceTransformer()),
    ('words', AddWordsTransformer()),
    ('header', AddHeaderAttributesTransformer()),
])
