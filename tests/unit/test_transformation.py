import unittest

from unittest import mock

from unittest.mock import patch, mock_open

import pandas as pd

from io import BytesIO, StringIO

from crisp_app.transformation import (
    read_input_data, read_input_config,
    create_target_cols, rename_target_cols, 
    convert_target_cols_dtypes, 
    manipulate_str_dtype_target_cols, 
    select_target_cols
)

class ReadInputConfigTestCase(unittest.TestCase):
    @mock.patch("builtins.open", mock_open(read_data="data"))
    @mock.patch("os.path.isfile")
    def test_read_input_config_positive(self, patched_isfile):
        patched_isfile.return_value = True

        result = read_input_config("dummy_config.yml")

        self.assertEqual(result, "data")

class ReadInputDataTestCase(unittest.TestCase):
    def test_read_input_data_positive(self):
        output = StringIO('col1\n1\n2\n3')

        df = read_input_data(output)

        pd.testing.assert_frame_equal(df, pd.DataFrame({"col1": [1, 2, 3]}))


class CreateTargetColsTestCase(unittest.TestCase):
    def test_create_target_cols_positive(self):
        config_dict = {'new_cols': {'col3': ["some_str", "another_str", "third_str"]}}

        raw_df = pd.DataFrame({"col1": [1, 2, 3],
                               "col2": ["string1", "string2", "string3"]})
        
        raw_df = create_target_cols(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [1, 2, 3],
                                                           "col2": ["string1", "string2", "string3"],
                                                           "col3": ["some_stranother_strthird_str", "some_stranother_strthird_str", "some_stranother_strthird_str"]}))

    def test_create_new_col_col_exists_positive(self):
        config_dict = {'new_cols': {'col3': ["col1", "col2"]}}

        raw_df = pd.DataFrame({"col1": [1, 2, 3],
                               "col2": ["string1", "string2", "string3"]})
        
        raw_df = create_target_cols(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [1, 2, 3],
                                                           "col2": ["string1", "string2", "string3"],
                                                           "col3": ["1-string1", "2-string2", "3-string3"]}))

class RenameTargetColsTestCase(unittest.TestCase):
    def test_rename_target_cols_positive(self):
        config_dict = {'renamed_cols': {'col1': 'renamed_col1',
                                        'col2': 'renamed_col2'}}

        raw_df = pd.DataFrame({"col1": [1, 2, 3],
                               "col2": ["string1", "string2", "string3"]})
        
        raw_df = rename_target_cols(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"renamed_col1": [1, 2, 3],
                                                           "renamed_col2": ["string1", "string2", "string3"]}))

class ConvertTargetColsDtypesTestCase(unittest.TestCase):
    def test_convert_target_cols_dtypes_positive(self):
        config_dict = {'dtype_cols': {'int': ['col1'],
                                        'str': ['col2']}}

        raw_df = pd.DataFrame({"col1": ["1", "2", "3"],
                               "col2": [1, 2, 3]})
        
        raw_df = convert_target_cols_dtypes(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [1, 2, 3],
                                                           "col2": ["1", "2", "3"]}))

class ManipulateStrDtypeTargetColsTestCase(unittest.TestCase):
    def test_manipulate_str_dtype_target_cols_positive(self):
        config_dict = {'str_dtype_cols_manipulation': {'proper_case': ['col1']}}

        raw_df = pd.DataFrame({"col1": ["some string", "another string", "a final string"]})
        
        raw_df = manipulate_str_dtype_target_cols(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": ["Some String", "Another String", "A Final String"]}))

class SelectTargetColsTestCase(unittest.TestCase):
    def test_manipulate_str_dtype_target_cols_positive(self):
        config_dict = {'select_cols': ['col1', 'col2', 'col3']}

        raw_df = pd.DataFrame({'col10': [1, 2, 3], 'col8': [4, 5, 6], 'col2':[7, 8, 9], 'col1': [0, 1, 2], 'col3': [3, 4, 5]})
        
        raw_df = select_target_cols(config_dict, raw_df)

        pd.testing.assert_frame_equal(raw_df, pd.DataFrame({"col1": [0, 1, 2], "col2": [7, 8, 9], "col3": [3, 4, 5]}))
