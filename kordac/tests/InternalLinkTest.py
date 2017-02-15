import markdown
import re
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.InternalLinkPattern import InternalLinkPattern
from kordac.tests.BaseTestCase import BaseTestCase

class InternalLinkTest(BaseTestCase):
    """Tests to check the 'internal-link' pattern works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'internal-link'
        self.ext = Mock()
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}

    def test_basic_usage(self):
        test_string = self.read_test_file('doc_example_basic_usage')

        processor = InternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('doc_example_basic_usage_expected').strip()
        self.assertEqual(expected_string, converted_test_string)
