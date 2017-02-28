import markdown
import re
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.GlossaryLinkPattern import GlossaryLinkPattern
from kordac.tests.ProcessorTest import ProcessorTest


class GlossaryLinkTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'glossary-link'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_single_word_term(self):
        test_string = self.read_test_file(self.processor_name, 'single_word_term.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'single_word_term_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_word_term(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_word_term.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_word_term_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_reference_text_given(self):
        test_string = self.read_test_file(self.processor_name, 'reference_text_given.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'reference_text_given_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_leading_inline_text(self):
        test_string = self.read_test_file(self.processor_name, 'leading_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'leading_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_trailing_inline_text(self):
        test_string = self.read_test_file(self.processor_name, 'trailing_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'trailing_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_leading_and_trailing_inline_text(self):
        test_string = self.read_test_file(self.processor_name, 'leading_and_trailing_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'leading_and_trailing_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_terms(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_terms.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_terms_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_reference_text(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_reference_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_reference_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

