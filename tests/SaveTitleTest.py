from kordac import Kordac
from kordac.processors.SaveTitlePreprocessor import SaveTitlePreprocessor
from tests.BaseTestCase import BaseTestCase

class SaveTitleTest(BaseTestCase):
    """Tests to check the 'save-title' preprocesser works as intended."""

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'save-title'
        self.converter = Kordac()

    def test_basic_usage(self):
        test_string = self.read_test_file('doc_example_basic_usage')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        expected_string = self.read_expected_output_file('doc_example_basic_usage_expected').strip()
        self.assertEqual(expected_string, converted_test_title)

    def test_multiple_headings(self):
        test_string = self.read_test_file('multiple_headings')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        expected_string = self.read_expected_output_file('multiple_headings_expected').strip()
        self.assertEqual(expected_string, converted_test_title)

    def test_multiple_level_one_headings(self):
        test_string = self.read_test_file('multiple_level_one_headings')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        expected_string = self.read_expected_output_file('multiple_level_one_headings_expected').strip()
        self.assertEqual(expected_string, converted_test_title)

    def test_no_headings(self):
        test_string = self.read_test_file('no_headings')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        self.assertIsNone(converted_test_title)

    def test_no_result_processor_off(self):
        test_string = self.read_test_file('doc_example_basic_usage')
        new_tags = self.converter.tag_defaults()
        new_tags.remove(self.tag_name)
        self.converter.update_tags(new_tags)
        result = self.converter.run(test_string)
        converted_test_title = result.title
        self.assertIsNone(converted_test_title)

    def test_level_two_heading(self):
        test_string = self.read_test_file('level_two_heading')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        expected_string = self.read_expected_output_file('level_two_heading_expected').strip()
        self.assertEqual(expected_string, converted_test_title)

    def test_no_heading_permalink(self):
        test_string = self.read_test_file('no_heading_permalink')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        self.assertIsNone(converted_test_title)

    def test_no_space_title(self):
        test_string = self.read_test_file('no_space_title')
        result = self.converter.run(test_string)
        converted_test_title = result.title
        expected_string = self.read_expected_output_file('no_space_title_expected').strip()
        self.assertEqual(expected_string, converted_test_title)
