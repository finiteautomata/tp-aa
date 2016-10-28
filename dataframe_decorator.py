#! coding: utf-8
"""Clase decoradora del dataframe."""
import scipy


class DataframeDecorator(object):
    u"""
    Decorador de dataframe.

    Tiene dos métodos más:
    - design_matrix: devuelve la matriz de diseño
    - dependent
    """

    def __init__(self, dataframe, freq_matrix):
        """
        Construye el dataframe.

        Argumentos:

        - dataframe: dataframe a ser decorado.
        """
        self.dataframe = dataframe
        self.freq_matrix = freq_matrix

    @property
    def design_matrix(self):
        u"""Devuelve matriz de diseño (variables independientes)."""
        df_data = self.dataframe._get_numeric_data().values

        return scipy.sparse.hstack([
            scipy.sparse.csr_matrix(df_data.astype('float64')),
            self.freq_matrix
        ])

    @property
    def outcomes(self):
        """Devuelve el vector de las predicciones (Y)."""
        target = (self.dataframe['class'] == 'spam')

        return target

    def __getattr__(self, name):
        u"""Implementa el método decorador."""
        return getattr(self.dataframe, name)
