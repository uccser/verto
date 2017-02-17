import markdown
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.SaveTitlePreprocessor import SaveTitlePreprocessor
from kordac.tests.BaseTestCase import BaseTestCase

class SaveTitleTest(BaseTestCase):
    """Tests to check the 'save-title' preprocesser works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'save-title'
        self.ext = Mock()
        self.ext.processor_info = BaseTestCase.loadProcessorInfo(self)

    def test_basic_usage(self):
        test_string = self.read_test_file('doc_example_basic_usage')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('doc_example_basic_usage_expected').strip()
        self.assertEqual(expected_string, self.kordac_extension.title)

    def test_multiple_headings(self):
        test_string = self.read_test_file('multiple_headings')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_headings_expected').strip()
        self.assertEqual(expected_string, self.kordac_extension.title)

    def test_multiple_level_one_headings(self):
        test_string = self.read_test_file('multiple_level_one_headings')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_level_one_headings_expected').strip()
        self.assertEqual(expected_string, self.kordac_extension.title)

    def test_no_headings(self):
        test_string = self.read_test_file('no_headings')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        self.assertIsNone(self.kordac_extension.title)

    def test_level_two_heading(self):
        test_string = self.read_test_file('level_two_heading')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('level_two_heading_expected').strip()
        self.assertEqual(expected_string, self.kordac_extension.title)

    def test_no_heading_permalink(self):
        test_string = self.read_test_file('no_heading_permalink')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        self.assertIsNone(self.kordac_extension.title)

    def test_no_space_title(self):
        test_string = self.read_test_file('no_space_title')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_space_title_expected').strip()
        self.assertEqual(expected_string, self.kordac_extension.title)

    # SYSTEM TESTS

    def test_no_result_processor_off(self):
        # Create Kordac extension without processor enabled
        kordac_extension = KordacExtension()
        test_string = self.read_test_file('doc_example_basic_usage')

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        self.assertIsNone(kordac_extension.title)
