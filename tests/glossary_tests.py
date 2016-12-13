
import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.glossary import *


class GlossaryLinkTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/glossary/{}.txt'

    # NTS should these functions end in true/false to match assert statment?
    def test_no_match(self):
        test_string = open(self.test_file_path.format('fail_string')).read()
        self.assertFalse(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        # TODO test longer strings

    def test_match_single_word_term(self):
        test_string = open(self.test_file_path.format('single_word_term')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_multiple_word_term(self):
        test_string = open(self.test_file_path.format('multiple_word_term')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_inline(self):
        test_string = open(self.test_file_path.format('inline_leading_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = open(self.test_file_path.format('inline_trailing_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))
        test_string = open(self.test_file_path.format('inline_leading_and_trailing_characters')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_matches_more_than_one_glossary_link(self):
        test_string = open(self.test_file_path.format('multiple_terms')).read()
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_correctly_parsed_inline(self):
        test_string = 'lots of leading characters {glossary-link term="binary search"}binary search{glossary-link end}'
        test_string = '{glossary-link term="binary search"}binary search{glossary-link end} a few trailing characters'
        test_string = 'here\'s some leading characters {glossary-link term="binary search"}binary search{glossary-link end} and here\'s a few trailing characters'
        pass

    def test_glossary_link_in_panel(self):
        pass

    def tearDown(self):
        self.md = None

# use this to test entire output matches expected
# print(markdown.markdown(test_string, extensions=[CSFGExtension()]))
