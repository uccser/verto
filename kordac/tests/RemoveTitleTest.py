import markdown
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.RemoveTitlePreprocessor import RemoveTitlePreprocessor
from kordac.tests.BaseTestCase import BaseTestCase

class RemoveTitleTest(BaseTestCase):
    """Tests to check the 'remove-title' preprocesser works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'remove-title'
        self.ext = Mock()
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)

    def test_basic_usage(self):
        test_string = self.read_test_file('doc_example_basic_usage')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('doc_example_basic_usage_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_headings(self):
        test_string = self.read_test_file('multiple_headings')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_headings_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_level_one_headings(self):
        test_string = self.read_test_file('multiple_level_one_headings')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_level_one_headings_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_no_headings(self):
        test_string = self.read_test_file('no_headings')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_headings_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_level_two_heading(self):
        test_string = self.read_test_file('level_two_heading')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('level_two_heading_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_no_heading_permalink(self):
        test_string = self.read_test_file('no_heading_permalink')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_heading_permalink_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_no_space_title(self):
        test_string = self.read_test_file('no_space_title')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_space_title_expected').strip()
        self.assertEqual(expected_string, converted_test_string)


    # SYSTEM TESTS

    def test_processor_off(self):
        # Create Kordac extension without processor enabled (off by default)
        kordac_extension = KordacExtension()
        test_string = self.read_test_file('processor_off')

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_expected_output_file('processor_off_expected')
        self.assertEqual(expected_string, converted_test_string)
