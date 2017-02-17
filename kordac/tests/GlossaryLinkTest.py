import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.GlossaryLinkBlockProcessor import GlossaryLinkBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest


class GlossaryLinkTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'glossary-link'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_patterns = ProcessorTest.loadProcessorPatterns(self)

    def test_match_false(self):
        test_string = self.read_test_file(self.processor_name, 'fail_string.md')
        self.assertFalse(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        # TODO test longer strings

    def test_match_single_word_term_true(self):
        test_string = self.read_test_file(self.processor_name, 'single_word_term.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_multiple_word_term_true(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_word_term.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        # TODO test more files with multiple terms

    def test_match_inline_true(self):
        test_string = self.read_test_file(self.processor_name, 'inline_leading_characters.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = self.read_test_file(self.processor_name, 'inline_trailing_characters.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = self.read_test_file(self.processor_name, 'inline_leading_and_trailing_characters.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_matches_more_than_one_glossary_link_true(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_terms.md')
        self.assertTrue(GlossaryLinkBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    # should parsing tests be in their own class?
    def test_correctly_parsed_inline(self):
        test_string = self.read_test_file(self.processor_name, 'inline_leading_characters.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension]) + '\n'
        expected_file_string = self.read_test_file(self.processor_name, 'inline_leading_characters_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

        test_string = self.read_test_file(self.processor_name, 'inline_trailing_characters.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension]) + '\n'
        expected_file_string = self.read_test_file(self.processor_name, 'inline_trailing_characters_expected.html', strip=True)
        # self.assertEqual(converted_test_string, expected_file_string)

        test_string = self.read_test_file(self.processor_name, 'inline_leading_and_trailing_characters.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension]) + '\n'
        expected_file_string = self.read_test_file(self.processor_name, 'inline_leading_and_trailing_characters_expected.html', strip=True)
        # self.assertEqual(converted_test_string, expected_file_string)

    def test_glossary_link_in_panel(self):
        pass
