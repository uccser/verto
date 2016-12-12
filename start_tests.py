
import unittest
import markdown
# import mdx_math

# from processors.panel import *
# from processors.comment import *
# from processors.video import *
# from processors.image import *
# from processors.interactive import *
# from processors.heading import *
# from processors.django import *
# from processors.glossary import *

# from tests.glossary_tests import *
# from glossary_tests import *

from glossary_tests import *
from markdown.extensions import Extension
from csfg_extension import CSFGExtension

from collections import defaultdict


TEST_FILES = ['algorithms']


def suite():
    # add all GlossayTests
    suite = unittest.makeSuite(GlossaryLinkTest, 'test') # order of tests by cmp()
    # suite.addTest(GlossaryLinkTest('test_match_true'))
    # suite.addTest(GlossaryLinkTest('test_match_false'))
    return suite



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)



