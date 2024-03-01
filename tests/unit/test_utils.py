import unittest
import pandas as pd

from crisp_app.utils import allowed_file, create_new_col
    
class AllowedFileTestCase(unittest.TestCase):
    def test_allowed_file_positive(self):
        result = allowed_file('input_data.csv', ['csv'])

        self.assertEqual(result, True)

    def test_allowed_file_negative(self):
        result = allowed_file('input_data.yml', ['csv'])

        self.assertEqual(result, False)

class CreateNewColTestCase(unittest.TestCase):
    def test_create_new_col_no_col_exists_positive(self):
        raw_df = pd.DataFrame({"col1": [1, 2, 3],
                               "col2": ["string1", "string2", "string3"]})
        
        raw_df = create_new_col(raw_df, "col3", ["some_str", "another_str", "third_str"])

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [1, 2, 3],
                                                           "col2": ["string1", "string2", "string3"],
                                                           "col3": ["some_stranother_strthird_str", "some_stranother_strthird_str", "some_stranother_strthird_str"]}))

    def test_create_new_col_col_exists_positive(self):
        raw_df = pd.DataFrame({"col1": [1, 2, 3],
                               "col2": ["string1", "string2", "string3"]})
        
        raw_df = create_new_col(raw_df, "col3", ["col1", "col2"])

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [1, 2, 3],
                                                           "col2": ["string1", "string2", "string3"],
                                                           "col3": ["1-string1", "2-string2", "3-string3"]}))