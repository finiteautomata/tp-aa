# -*- coding: utf-8 -*-
"""Clase que se encarga de construir el dataframe en base a los ham y spam."""
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import pandas as pd


class DataFrameBuilder(object):
    """
    Construye un dataframe en base al dataset de spam y ham.

    Uso:

    > ham_txt = json.load(open('data/ham_dev.json'))
    > spam_txt = json.load(open('data/spam_dev.json'))
    > builder = DataFrameBuilder(ham=ham_txt, spam=spam_txt)
    > df = builder.build()
    """

    def __init__(self):
        """Constructor."""
        self.list_of_attributes = []

    def build(self, spam, ham):
        u"""
        Construye el dataframe.

        Devuelve el dataframe ya construído
        """
        klass = ['spam'] * len(spam) + ['ham'] * len(ham)

        self.df = pd.DataFrame({'text': spam + ham, 'class': klass})

        self.add_attribute(len, 'len')
        self.add_attribute(lambda t: t.count(' '), 'spaces')
        self.add_word_attribute("<html>", "has_html")
        self.add_word_attribute("Original Message", "has_original_message")

        # este habría que refinarlo un poco
        self.add_word_attribute("multipart", lower=True)

	greetings = ["dear","Friend","hello"]

	investment = ["$","earn","investment","profit","profits","credit","opportunity","income","cost"]

	promotions = ["promotion","why pay more?","f r e e","click","add"]

	sex = ["meet singles","viagra","sex","penis","vagina","pussy","fuck","girl","erect","enlargement"]

	words = ["free", "cc:", "gif", "help", "photo", "video",
                     "http", "dollar", "million", "|","nigeria", "million","password","of","bill","it's time","sale","hi","-->","weight","lose","administrator","order","clearance","meet singles"]

	categories = [greetings,investment,promotions,sex,word]	
	
	for category in categories:
		self.add_atributes_from(category)


#        for word in ["free", "cc:", "gif", "help", "photo", "video", "http", "dollar", "million", "|","nigeria", "million","password","of","bill","it's time","sale","hi","-->","weight","lose","administrator","order","clearance","meet singles"]:
 #           self.add_word_attribute(word, lower=True)
	

        return self.df


    def add_atributes_from(self,anArray):

	for word in anArray:
		self.add_word_attribute(word,lower=True)


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
