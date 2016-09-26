#! coding:utf-8
u"""Archivo de configuración."""

import os
import warnings
warnings.filterwarnings('ignore',
                        message='Changing the shape of non-C contiguous array')


def project_dir():
    """Calcula el directorio del proyecto."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(current_dir)


root_dir = project_dir()
cache_dir = os.path.join(root_dir, "cache")
data_dir = os.path.join(root_dir, "data")

ham_dev_path = os.path.join(data_dir, "ham_dev.json")
ham_test_path = os.path.join(data_dir, "ham_test.json")

spam_dev_path = os.path.join(data_dir, "spam_dev.json")
spam_test_path = os.path.join(data_dir, "spam_test.json")

dev_dataframe_path = os.path.join(cache_dir, "dataframe.pickle")
test_dataframe_path = os.path.join(cache_dir, "dataframe.test.pickle")
