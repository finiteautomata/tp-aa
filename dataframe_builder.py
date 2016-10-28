# -*- coding: utf-8 -*-
"""Clase que se encarga de construir el dataframe en base a los ham y spam."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import random

import dateutil
import pandas as pd
import json
import config
import re
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from dataframe_decorator import DataframeDecorator


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
                 dataframe_path=config.dev_dataframe_path,
                 tdidf_path=config.dev_tdidf_path):
        """Constructor."""
        self.list_of_attributes = []
        self.cache = cache
        self.delete_text = delete_text
        self.dataframe_path = dataframe_path
        self.tdidf_path = tdidf_path

    def build(self,
              spam_path=config.spam_dev_path, ham_path=config.ham_dev_path):
        u"""
        Construye el dataframe.

        Argumentos:

        - spam: lista de mails spam
        - ham: lista de mails ham
        - cache: intenta usar pickle
        """
        self.df = self.freq_matrix = None
        self.columns_to_remove = ['text']

        if self.cache:
            try:
                print "Buscando dataframe en {}".format(self.dataframe_path)
                self.df = pd.read_pickle(self.dataframe_path)
                print "Encontrado. Dimensiones: {}".format(self.df.shape)
                print "Buscando matriz tdidf en {}".format(self.tdidf_path)
                self.freq_matrix = joblib.load(self.tdidf_path)
                print "Encontrado. Dimensiones: {}".format(
                    self.freq_matrix.shape)
            except:
                print "Hubo un error cargando los datos"
                pass

        if self.df is None or self.freq_matrix is None:
            self.build_from_scratch(spam_path=spam_path, ham_path=ham_path)

        return DataframeDecorator(self.df, self.freq_matrix)

    def build_from_scratch(self, spam_path, ham_path):
        u"""Construye el dataframe desde 0."""
        print "Armando dataframe..."
        spam = json.load(open(spam_path))
        ham = json.load(open(ham_path))

        self.build_raw(spam, ham)
        print "Dataframe construído"
        print "Armando matriz de frecuencias..."
        self.build_frequency_matrix()
        print "Construída"

        if self.delete_text:
            self.delete_columns()

        if self.cache:
            self.df.to_pickle(self.dataframe_path)
            print "Dataframe guardado en {}".format(self.dataframe_path)
            joblib.dump(self.freq_matrix, self.tdidf_path)
            print "TD-IDF guardado en {}".format(self.tdidf_path)

    def build_frequency_matrix(self):
        """Construyo matriz de frecuencias con td-idf."""
        print "Construyendo matriz de frecuencias..."
        transformer = TfidfVectorizer(max_features=4000)
        self.freq_matrix = transformer.fit_transform(self.df.payload)

    def delete_columns(self):
        """Borro columnas innecesarias."""
        # Saco text porque pesa MUCHO
        try:
            del self.df.parsed_text
            del self.df.payload
            for column in self.columns_to_remove:
                self.df.drop(column, axis=1, inplace=True)
        except:
            print "Problema destruyendo columnas innecesarias"

    def build_raw(self, spam, ham):
        u"""Construye el dataframe con todos los datos."""
        self.add_header_attributes()
        self.add_date_attributes()

        return self.df

    def add_text_and_payload(self):
        """Agrego text y payload al df."""
        def get_text_payload(mail):
            payload = mail.get_payload()

            if type(payload) is str:
                return payload
            elif type(payload) is list:
                return ",".join([get_text_payload(m) for m in payload])
            else:
                raise Exception("Tipo de payload ni string ni lista")



        self.df.parsed_text = self.df.text.apply(
            lambda t: parser.parsestr(t.encode('utf-8')))

        self.df.payload = self.df.parsed_text.apply(get_text_payload)


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

    def add_date_attributes(self):
        """Agrega atributos de fecha.

        OBS: Hay muchos mails sin fechas, ergo sin atributos como hora, etc

        Para esos casos, metemos valores random. No es lo mejor, lo sabemos
        pero no pudimos hacer andar el Imputer

        """
        def parse_date(parsed_mail):
            try:
                date = parsed_mail.get('Date') or parsed_mail.get('date')
                return dateutil.parser.parse(date, fuzzy_with_tokens=True)[0]
            except:
                return None

        def get_hour(date):
            if date:
                return date.hour + date.minute / 60.0
            else:
                return random.uniform(0, 24)

        def get_weekday(date):
            if date:
                return date.weekday()
            else:
                return random.choice(range(6))

        def get_year(date):
            if date:
                return date.year
            else:
                return random.choice(range(1999, 2010))

        self.df['date'] = self.df.parsed_text.apply(parse_date)
        self.df['hour'] = self.df.date.apply(get_hour)
        self.df['hour_is_normal'] = self.df['hour'].apply(
            lambda h: h >= 6 and h <= 20
        )
        self.df['weekday'] = self.df.date.apply(get_weekday)
        self.df['is_weekend'] = self.df['weekday'] >= 5
        self.df['year'] = self.df.date.apply(get_year)
        self.df['suspicious_year'] = self.df.year.apply(
            lambda y: y >= 2015 or y <= 1995
        )

        self.columns_to_remove += ['date']
