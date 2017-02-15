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

    def test_long_path(self):
        test_string = self.read_test_file('long_path')

        processor = InternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('long_path_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_links(self):
        test_string = self.read_test_file('multiple_links')

        processor = InternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_links_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_http_schema(self):
        test_string = self.read_test_file('http_schema')

        processor = InternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('http_schema_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_http_text(self):
        test_string = self.read_test_file('http_text')

        processor = InternalLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('http_text_expected').strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_https_schema(self):
        pass

    def test_https_text(self):
        pass

    def test_ignore_ftp_schema(self):
        pass

    def test_ftp_text(self):
        pass

    def test_ignore_ftps_schema(self):
        pass

    def test_ftps_text(self):
        pass

    def test_ignore_mailto_schema(self):
        pass

    def test_mailto_text(self):
        pass

    def test_ignore_news_schema(self):
        pass

    def test_news_text(self):
        pass
