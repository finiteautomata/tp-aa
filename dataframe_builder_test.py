import unittest

from dataframe_builder import DataFrameBuilder


class DataframeBuilderTest(unittest.TestCase):
    def test_it_returns_a_dataframe_with_text_column(self):
        builder = DataFrameBuilder()

        dataframe = builder.build(spam=['spam1'], ham=['ham1'])

        self.assertItemsEqual(dataframe.text, ['spam1', 'ham1'])

    def test_it_sets_class_properly(self):
        builder = DataFrameBuilder()

        df = builder.build(spam=['bad', 'bad'], ham=['ham1'])

        self.assertItemsEqual(df[df.text == "bad"]['class'], ['spam', 'spam'])

    def test_it_adds_len_column(self):
        builder = DataFrameBuilder()

        df = builder.build(spam=[], ham=['this is a mail'])

        self.assertEqual(df.loc[0, 'len'], len(df.loc[0, 'text']))

if __name__ == '__main__':
    unittest.main()
