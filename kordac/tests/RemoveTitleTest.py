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
