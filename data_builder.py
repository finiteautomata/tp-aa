# -*- coding: utf-8 -*-
"""Clase que se encarga de construir el dataframe en base a los ham y spam."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import email
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

    Devuelve un dataframe con columnas:

    text: tiene el texto plano del email

    """

    def get_text_payload(self, mail):
        """Devuelve el cuerpo del mail."""
        payload = mail.get_payload()

        if type(payload) is str:
            return payload
        elif type(payload) is list:
            return ",".join([self.get_text_payload(m) for m in payload])
        else:
            raise Exception("Tipo de payload ni string ni lista")

    def build(self,
              spam_path=config.spam_dev_path, ham_path=config.ham_dev_path):
        u"""Construye el dataframe desde 0."""
        spam = json.load(open(spam_path))
        ham = json.load(open(ham_path))

        klass = [True] * len(spam) + [False] * len(ham)

        parser = email.parser.Parser()

        text = spam + ham

        df = pd.DataFrame({
            'parsed_emails': [parser.parsestr(t.encode('utf-8')) for t in text]
        })

        # Agrego cuerpo del email
        df['payload'] = df.parsed_emails.apply(self.get_text_payload)

        return df, np.array(klass)
