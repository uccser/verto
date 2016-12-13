
import unittest
import markdown
from markdown.extensions import Extension
from collections import defaultdict

from tests.glossary_tests import *


class BaseTestCase(unittest.TestCase):
    """
    Base test
    """
    # could create the md instance here?
    pass


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



