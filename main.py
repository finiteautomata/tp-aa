# -*- coding: utf-8 -*-
# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import json
import random
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score


# Los siguientes cuatro imports los agregamos para poder graficar los arboles generados...
from sklearn.externals.six import StringIO  
import pydot 
from sklearn import tree
from IPython.display import Image  

#import numpy as np
from collections import Counter
import pylab


# Leo los mails (poner los paths correctos).
ham_txt= json.load(open('data/ham_dev.json'))
spam_txt= json.load(open('data/spam_dev.json'))

# Armo un dataset de Pandas
# http://pandas.pydata.org/

#
# JM:
# Esto crea un data frame, que básicamente es una matriz 'adornada', donde se le pueden poner nombres a las columnas y a las filas.
# Si quieren investigar un poco cómo se usan, fíjense en http://pandas.pydata.org/pandas-docs/stable/indexing.html, por ejemplo

df = pd.DataFrame(ham_txt+spam_txt, columns=['text'])

df['class'] = ['ham' for _ in range(len(ham_txt))]+['spam' for _ in range(len(spam_txt))]

# Extraigo dos atributos simples:
# 1) Longitud del mail.
df['len'] = map(len, df.text)

# 2) Cantidad de espacios en el mail.
def count_spaces(txt):
    return txt.count(" ")
df['count_spaces'] = map(count_spaces, df.text)
# Éste lo agregué yo...subió a 90% :o


list_of_attributes = ['len', 'count_spaces']


def add_attribute(df, fun, column_name):
    """
    Agrega una columna al dataframe df que consiste en ver si word esta presente en la columna df.text

    Atributos:

    - df: dataset de Pandas
    - word: palabra a buscar en el texto
    - column_name: Opcional. Nombre de la columna a crear en el dataframe 
    - lower: Busco case insensitive (False por defecto) 
    """

    global list_of_attributes
    list_of_attributes.append(column_name)
    df[column_name] = map(fun, df.text)


def add_word_attribute(df, word, column_name=None, lower=False):
    """
    Agrega una columna al dataframe df que consiste en ver si word esta presente en la columna df.text

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

    add_attribute(df, fun, column_name)




add_word_attribute(df, "<html>", "has_html")
add_word_attribute(df, "Original Message", "has_original_message")
add_word_attribute(df, "free", lower=True)

add_word_attribute(df, "cc:", lower=True)

for word in ["gif", "help", "http", "dollar", "million", "|"]:
    add_word_attribute(df, word)


# Preparo data para clasificar
X = df[list_of_attributes].values
y = df['class']

# Elijo mi clasificador.
clfWithEntropy = DecisionTreeClassifier( criterion="entropy")
clfWithGini = DecisionTreeClassifier( criterion="gini")

# Ejecuto el clasificador entrenando con un esquema de cross validation
# de 10 folds.
resWithEntropy = cross_val_score(clfWithEntropy, X, y, cv=10)
resWithGini = cross_val_score(clfWithGini, X, y, cv=10)

print np.mean(resWithEntropy), np.std(resWithEntropy)
print np.mean(resWithGini), np.std(resWithGini)
# salida: 0.783040309346 0.0068052434174  (o similar)

#arbolito = clf.fit(X,y)

#dot_data = StringIO() 
#tree.export_graphviz(arbolito, out_file=dot_data) 

#tree.export_graphviz(arbolito,out_file='tree.dot') 

# Para pasar el .dot a un archivo visualizable  correr alguna de las siguientes lineas
# $ dot -Tps tree.dot -o tree.ps      (PostScript format)
# $ dot -Tpng tree.dot -o tree.png    (PNG format)


#graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
#Image(graph.create_png()) 


