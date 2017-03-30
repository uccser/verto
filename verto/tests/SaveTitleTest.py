import markdown
from unittest.mock import Mock
from verto.VertoExtension import VertoExtension
from verto.processors.SaveTitlePreprocessor import SaveTitlePreprocessor
from verto.tests.ProcessorTest import ProcessorTest

class SaveTitleTest(ProcessorTest):
    """Tests to check the 'save-title' preprocesser works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'save-title'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_basic_usage(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True).strip()
        self.assertEqual(expected_string, self.verto_extension.title)

    def test_multiple_headings(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_headings.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, self.verto_extension.title)

    def test_multiple_level_one_headings(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, self.verto_extension.title)

    def test_no_headings(self):
        test_string = self.read_test_file(self.processor_name, 'no_headings.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        self.assertIsNone(self.verto_extension.title)

    def test_level_two_heading(self):
        test_string = self.read_test_file(self.processor_name, 'level_two_heading.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'level_two_heading_expected.html', strip=True).strip()
        self.assertEqual(expected_string, self.verto_extension.title)

    def test_no_heading_permalink(self):
        test_string = self.read_test_file(self.processor_name, 'no_heading_permalink.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        self.assertIsNone(self.verto_extension.title)

    def test_no_space_title(self):
        test_string = self.read_test_file(self.processor_name, 'no_space_title.md')

        processor = SaveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_space_title_expected.html', strip=True).strip()
        self.assertEqual(expected_string, self.verto_extension.title)

    # SYSTEM TESTS

    def test_no_result_processor_off(self):
        # Create Verto extension without processor enabled
        verto_extension = VertoExtension()
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        self.assertIsNone(verto_extension.title)
