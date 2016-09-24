#! coding:utf-8
u"""Archivo de configuración."""

import os


def project_dir():
    """Calcula el directorio del proyecto."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(current_dir)


root_dir = project_dir()
cache_dir = os.path.join(root_dir, "cache/")
data_dir = os.path.join(root_dir, "data/")

ham_dev_path = os.path.join(data_dir, "ham_dev.json")
spam_dev_path = os.path.join(data_dir, "spam_dev.json")
dataframe_path = os.path.join(cache_dir, "dataframe.pickle")
