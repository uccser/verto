import markdown
import re
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GlossaryLinkPattern import GlossaryLinkPattern
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.tests.ProcessorTest import ProcessorTest


class GlossaryLinkTest(ProcessorTest):
    '''The GlossaryLink processor changes the extension so to output
    a special result. Special things to note about this processor is
    it is inline, and stores references found in the extension class.
    '''

    def __init__(self, *args, **kwargs):
        '''Setup basic information for asset directory.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'glossary-link'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_single_word_term(self):
        '''Tests that a single glossary link functions as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'single_word_term.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'single_word_term_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'quicksort': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_multiple_word_term(self):
        '''Tests that multiple glossary links are processed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_word_term.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_word_term_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'digital-signature': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_reference_text_given(self):
        '''Tests that the reference argument is processed and that details are stored in the final result.
        '''
        test_string = self.read_test_file(self.processor_name, 'reference_text_given.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'reference_text_given_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'chomsky-hierarchy':
                [('Formal languages', 'glossary-chomsky-hierarchy')]
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_leading_inline_text(self):
        '''Tests that glossary links are matched and processed even when there is text before the tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'leading_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'leading_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'grammar': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_trailing_inline_text(self):
        '''Tests that glossary links are matched and processed even when there is text after the tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'trailing_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'trailing_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'finite state automaton': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_leading_and_trailing_inline_text(self):
        '''Tests that glossary links are matched and processed even when there is text before and after the tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'leading_and_trailing_inline_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'leading_and_trailing_inline_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'Regular expression': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_multiple_terms(self):
        '''Tests that multiple glossary tags are matched and that tags with the reference argument store information for the final result.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_terms.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_terms_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'grammar': [],
            'regular-expression': [],
            'finite-state-automaton':
                [('Formal languages', 'glossary-finite-state-automaton')]
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_multiple_reference_text(self):
        '''Tests that when the reference argument is used in multiple tags that all references are stored for the final verto result.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_reference_text.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_reference_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'hello': [],
            'algorithm':
                [('computer program', 'glossary-algorithm'),
                 ('algorithm cost', 'glossary-algorithm-2'),
                 ('searching algorithms', 'glossary-algorithm-3'),
                 ('sorting algorithms', 'glossary-algorithm-4')]
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_custom_arguments_reference_text_true(self):
        '''Tests that glossary tag is rendered correctly when reference text is required.
        '''
        test_string = self.read_test_file(self.processor_name, 'reference_text_true.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'reference_text_true_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'chomsky-hierarchy':
                [('Formal languages', 'glossary-chomsky-hierarchy')]
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_custom_arguments_reference_text_true_not_provided(self):
        '''Tests to ensure that correct error is raised when reference text is required and not provided.
        '''
        custom_argument_rules = {
            "glossary-link": {
                "reference-text": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'reference_text_true_not_provided.md')
        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''A basic example of common useage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = self.verto_extension.glossary_terms
        expected_glossary_terms = {
            'algorithm': []
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)

    def test_doc_example_override_html(self):
        '''A basic example of overriding the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        glossary_terms = verto_extension.glossary_terms
        expected_glossary_terms = {
            'algorithm':
                [('Software Engineering', 'glossary-algorithm')]
        }
        self.assertDictEqual(expected_glossary_terms, glossary_terms)
