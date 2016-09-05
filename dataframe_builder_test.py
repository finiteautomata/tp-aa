import unittest

from dataframe_builder import DataFrameBuilder


class DataframeBuilderTest(unittest.TestCase):
    def test_it_returns_a_dataframe_with_text_column(self):
        builder = DataFrameBuilder(spam=['spam1'], ham=['ham1'])

        dataframe = builder.build()

        self.assertItemsEqual(dataframe.text, ['spam1', 'ham1'])

    def test_it_sets_class_properly(self):
        builder = DataFrameBuilder(spam=['bad', 'bad'], ham=['good'])

        df = builder.build()

        self.assertItemsEqual(df[df.text == "bad"]['class'], ['spam', 'spam'])

    def test_it_adds_len_column(self):
        builder = DataFrameBuilder(spam=[], ham=['this is a mail'])

        df = builder.build()

        self.assertEqual(df.loc[0, 'len'], len(df.loc[0, 'text']))

if __name__ == '__main__':
    unittest.main()
