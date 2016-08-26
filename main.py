# Aprendizaje Automatico - DC, FCEN, UBA
# Segundo cuatrimestre 2016

import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score

# Leo los mails (poner los paths correctos).
ham_txt= json.load(open('data/ham_txt.json'))
spam_txt= json.load(open('data/spam_txt.json'))

# Imprimo un mail de ham y spam como muestra.
print ham_txt[0]
print "------------------------------------------------------"
print spam_txt[0]
print "------------------------------------------------------"

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
df['has_html'] = map(lambda text: "<html>" in text, df.text)

# Preparo data para clasificar
X = df[['len', 'count_spaces', 'has_html']].values
y = df['class']

# Elijo mi clasificador.
clf = DecisionTreeClassifier()

# Ejecuto el clasificador entrenando con un esquema de cross validation
# de 10 folds.
res = cross_val_score(clf, X, y, cv=10)
print np.mean(res), np.std(res)
# salida: 0.783040309346 0.0068052434174  (o similar)
