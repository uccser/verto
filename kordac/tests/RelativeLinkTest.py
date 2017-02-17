import markdown
import re
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.RelativeLinkPattern import RelativeLinkPattern
from kordac.tests.ProcessorTest import ProcessorTest

class RelativeLinkTest(ProcessorTest):
    """Tests to check the 'relative-link' pattern works as intended."""

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'relative-link'
        self.ext = Mock()
        self.ext.processor_patterns = ProcessorTest.loadProcessorPatterns(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_basic_usage(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_long_path(self):
        test_string = self.read_test_file(self.processor_name, 'long_path.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'long_path_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_links(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_links.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_links_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_http_schema(self):
        test_string = self.read_test_file(self.processor_name, 'http_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'http_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_http_text(self):
        test_string = self.read_test_file(self.processor_name, 'http_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'http_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_https_schema(self):
        test_string = self.read_test_file(self.processor_name, 'https_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'https_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_https_text(self):
        test_string = self.read_test_file(self.processor_name, 'https_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'https_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_ftp_schema(self):
        test_string = self.read_test_file(self.processor_name, 'ftp_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftp_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ftp_text(self):
        test_string = self.read_test_file(self.processor_name, 'ftp_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftp_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_ftps_schema(self):
        test_string = self.read_test_file(self.processor_name, 'ftps_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftps_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ftps_text(self):
        test_string = self.read_test_file(self.processor_name, 'ftps_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'ftps_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_ignore_mailto_schema(self):
        test_string = self.read_test_file(self.processor_name, 'mailto_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'mailto_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_mailto_text(self):
        test_string = self.read_test_file(self.processor_name, 'mailto_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'mailto_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)


    def test_ignore_news_schema(self):
        test_string = self.read_test_file(self.processor_name, 'news_schema.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'news_schema_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_news_text(self):
        test_string = self.read_test_file(self.processor_name, 'news_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'news_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_www_text(self):
        test_string = self.read_test_file(self.processor_name, 'www_text.md')

        processor = RelativeLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'www_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)
