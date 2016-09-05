# -*- coding: utf-8 -*-
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import pandas as pd


class DataFrameBuilder(object):
    def __init__(self, spam, ham):
        self.spam = spam
        self.ham = ham

    def build(self):
        klass = ['spam'] * len(self.spam) + ['ham'] * len(self.ham)

        self.df = pd.DataFrame({'text': self.spam + self.ham, 'class': klass})

        self.list_of_attributes = []

        self.add_attribute(len, 'len')
        self.add_attribute(lambda t: t.count(' '), 'spaces')
        self.add_word_attribute("<html>", "has_html")
        self.add_word_attribute("Original Message", "has_original_message")
        self.add_word_attribute("free", lower=True)
        self.add_word_attribute("cc:", lower=True)

        for word in ["gif", "help", "http", "dollar", "million", "|"]:
            self.add_word_attribute(word)

        return self.df

    def add_attribute(self, fun, column_name):
        """
        Agrega columna al dataframe df que consiste en aplicar fun a df.text

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
        Agrega una columna al dataframe df que consiste en ver
        si word esta presente en la columna df.text

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
