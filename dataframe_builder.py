# -*- coding: utf-8 -*-
"""Clase que se encarga de construir el dataframe en base a los ham y spam."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import email
import pandas as pd
import json
import config
from dataframe_decorator import DataframeDecorator


def load_dev_dataframe(**kwargs):
    """Carga el dataframe de dev."""
    builder = DataFrameBuilder(**kwargs)
    return builder.build()


def load_test_dataframe(**kwargs):
    """Carga el dataframe de test."""
    builder = DataFrameBuilder(**kwargs)

    return builder.build(
        spam_path=config.spam_test_path,
        ham_path=config.ham_test_path
    )


class DataFrameBuilder(object):
    """
    Construye un dataframe en base al dataset de spam y ham.

    Uso:

    > ham_txt = json.load(open('data/ham_dev.json'))
    > spam_txt = json.load(open('data/spam_dev.json'))
    > builder = DataFrameBuilder(ham=ham_txt, spam=spam_txt)
    > df = builder.build()
    """

    def __init__(self, cache=True, delete_text=True,
                 dataframe_path=config.dev_dataframe_path):
        """Constructor."""
        self.list_of_attributes = []
        self.cache = cache
        self.delete_text = delete_text
        self.dataframe_path = dataframe_path

    def build(self,
              spam_path=config.spam_dev_path, ham_path=config.ham_dev_path):
        u"""
        Construye el dataframe.

        Argumentos:

        - spam: lista de mails spam
        - ham: lista de mails ham
        - cache: intenta usar pickle
        """
        self.df = None

        if self.cache:
            try:
                print "Buscando dataframe en {}".format(self.dataframe_path)
                self.df = pd.read_pickle(self.dataframe_path)
                print "Encontrado. Dimensiones: {}".format(self.df.shape)
            except:

                pass

        if self.df is None:
            print "Armando dataframe..."
            spam = json.load(open(spam_path))
            ham = json.load(open(ham_path))

            self.build_from_scratch(spam, ham)

        return DataframeDecorator(self.df)

    def build_from_scratch(self, spam, ham):
        u"""Construye el dataframe desde 0."""
        klass = ['spam'] * len(spam) + ['ham'] * len(ham)

        parser = email.parser.Parser()

        self.columns_to_be_removed = ['text', 'parsed_text']

        self.df = pd.DataFrame({'text': spam + ham, 'class': klass})
        self.df.parsed_text = self.df.text.apply(
            lambda t: parser.parsestr(t.encode('utf-8')))

        self.add_content_type_columns()

        self.add_attribute(len, 'len')
        self.add_attribute(lambda t: t.count(' '), 'spaces')
        self.add_word_attribute("<html>", "has_html")
        self.add_word_attribute("Original Message", "has_original_message")

        # este habría que refinarlo un poco

        greetings = ["dear", "friend", "hello"]

        investment = [
            "$", "earn", "investment", "profit", "profits", "credit",
            "opportunity", "income", "cost"
        ]

        promotions = ["promotion", "why pay more?", "f r e e", "click", "add"]

        sex = [
            "meet singles", "viagra", "sex", "penis", "vagina", "pussy",
            "fuck", "girl", "erect", "enlargement"
        ]

        words = [
            "free", "cc:", "gif", "help", "photo", "video", "http", "dollar",
            "million", "|", "nigeria", "million", "password", "of", "bill",
            "it's time", "sale", "hi", "-->", "weight", "lose",
            "administrator", "order", "clearance", "meet singles"
        ]

        categories = [greetings, investment, promotions, sex, words]

        for category in categories:
            self.add_atributes_from(category)

        if self.delete_text:
            # Saco text porque pesa MUCHO
            for column in self.columns_to_be_removed:
                self.df.drop(column, axis=1, inplace=True)

        if self.cache:
            self.df.to_pickle(self.dataframe_path)
            print "Dataframe guardado en {}".format(self.dataframe_path)
            print "Dimensiones: {}".format(self.df.shape())

        return self.df

    def add_atributes_from(self, an_array):
        """Agrega los word attributes para cada elemento del array."""
        for word in an_array:
            self.add_word_attribute(word, lower=True)

    def add_content_type_columns(self):
        """Agrego todas las columnas relacionadas a content type."""
        content_type = self.df.parsed_text.apply(
            lambda t: t.get_content_type())

        types = [
            'multipart/mixed', 'text/html', 'multipart/alternative',
            'text/plain', 'multipart/related', 'multipart/report',
            'text/plain charset="us-ascii"', 'text/html charset=iso-8859-1',
            'application/vnd.ms-excel', 'message/rfc822', 'text/enriched',
            'text/richtext', 'image/pjpeg', 'application/msword',
            'application/octet-stream']

        for ctype in types:
            self.df[ctype] = content_type.apply(
                lambda t: ctype in t)

    def add_attribute(self, fun, column_name):
        """
        Agrega columna al dataframe df que consiste en aplicar fun a df.text.

        Atributos:

        - df: dataset de Pandas
        - word: palabra a buscar en el texto
        - column_name: Opcional. Nombre de la columna a crear en el dataframe
        - lower: Busco case insensitive (False por defecto)
        """
        self.list_of_attributes.append(column_name)
        self.df[column_name] = map(fun, self.df.text)

    def add_word_attribute(self, word, column_name=None, lower=False):
        """
        Agrega columna al dataframe df que cuenta ocurrencias de word.

        Atributos:

        - df: dataset de Pandas
        - word: palabra a buscar en el texto
        - column_name: Opcional. Nombre de la columna a crear en el dataframe
        - lower: Busco case insensitive (False por defecto)
        """
        column_name = column_name or ("has_" + word)

        def fun(text):
            if lower:
                return text.lower().count(word)
            else:
                return text.count(word)

        self.add_attribute(fun, column_name)
