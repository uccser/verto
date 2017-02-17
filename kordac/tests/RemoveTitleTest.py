import markdown
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.RemoveTitlePreprocessor import RemoveTitlePreprocessor
from kordac.tests.ProcessorTest import ProcessorTest

class RemoveTitleTest(ProcessorTest):
    """Tests to check the 'remove-title' preprocesser works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'remove-title'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_basic_usage(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_headings(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_level_one_headings(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_no_headings(self):
        test_string = self.read_test_file(self.processor_name, 'no_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_headings_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_level_two_heading(self):
        test_string = self.read_test_file(self.processor_name, 'level_two_heading.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'level_two_heading_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_heading_permalink(self):
        test_string = self.read_test_file(self.processor_name, 'no_heading_permalink.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_heading_permalink_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_space_title(self):
        test_string = self.read_test_file(self.processor_name, 'no_space_title.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_space_title_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)


    # SYSTEM TESTS

    def test_processor_off(self):
        # Create Kordac extension without processor enabled (off by default)
        kordac_extension = KordacExtension()
        test_string = self.read_test_file(self.processor_name, 'processor_off.md')

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'processor_off_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
