#! coding: utf-8
"""Clase decoradora del dataframe."""


class DataframeDecorator(object):
    u"""
    Decorador de dataframe.

    Tiene dos métodos más:
    - design_matrix: devuelve la matriz de diseño
    - dependent
    """

    def __init__(self, dataframe):
        """
        Construye el dataframe.

        Argumentos:

        - dataframe: dataframe a ser decorado.
        """
        self.dataframe = dataframe

    @property
    def design_matrix(self):
        """Devuelve la matriz de las variables dependientes (X)."""
        columns = self.dataframe.columns
        attributes = columns[columns != 'class']

        matrix = self.dataframe[attributes].values

        return matrix

    @property
    def outcomes(self):
        """Devuelve el vector de las predicciones (Y)."""
        target = (self.dataframe['class'] == 'spam')

        return target

    def __getattr__(self, name):
        u"""Implementa el método decorador."""
        return getattr(self.dataframe, name)
