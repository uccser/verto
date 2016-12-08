
import unittest
import markdown
from markdown.extensions import Extension

from test import CSFGExtension

from processors.glossary import *
from processors.thing import *
# from tests import glossary

# {glossary-link term="binary search"}binary search{glossary-link end}

class GlossaryLinkTest(unittest.TestCase):

    def test_not_none(self):
        md = markdown.Markdown()
        # test_string = "this is a test string"
        test_string = '{glossary-link term="binary search"}binary search{glossary-link end}'
        print(GlossaryLinkBlockProcessor(md.parser).test(None, test_string))
        assert GlossaryLinkBlockProcessor(md.parser).test(None, test_string) is not False


if __name__=='__main__':
    unittest.main()
