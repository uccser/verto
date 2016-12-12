
import markdown
import unittest
from csfg_extension import CSFGExtension

from processors.glossary import *

# {glossary-link term="binary search"}binary search{glossary-link end}

class GlossaryLinkTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])

    def test_match_true(self):
        test_string = '{glossary-link term="binary search"}binary search{glossary-link end}'
        self.assertTrue(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_false(self):
        test_string = 'this is a test'
        self.assertFalse(GlossaryLinkBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def tearDown(self):
        self.md = None

# use this to test entire output matches expected
# print(markdown.markdown(test_string, extensions=[CSFGExtension()]))
