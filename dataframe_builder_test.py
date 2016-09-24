#! coding: utf-8
"""Tests para DataframeBuilder."""
import unittest
import numpy as np
from dataframe_builder import DataFrameBuilder


class DataframeBuilderTest(unittest.TestCase):
    """Tests para DataframeBuilder."""

    def test_it_sets_class_properly(self):
        builder = DataFrameBuilder(cache=False)

        df = builder.build_from_scratch(spam=['bad', 'bad'], ham=['ham1'])

        self.assertEqual(np.count_nonzero(df['class'] == 'spam'), 2)

    def test_it_adds_len_column(self):
        builder = DataFrameBuilder(cache=False)

        df = builder.build_from_scratch(spam=[], ham=['this is a mail'])

        self.assertEqual(df.loc[0, 'len'], len('this is a mail'))

    def test_it_returns_something_answering_design_matrix(self):
        builder = DataFrameBuilder(cache=False)

        df = builder.build_from_scratch(spam=[], ham=['this is a mail'])




if __name__ == '__main__':
    unittest.main()
