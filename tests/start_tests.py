import unittest
import markdown
from markdown.extensions import Extension
from collections import defaultdict

from tests.glossary_tests import *
from tests.panel_tests import *


class BaseTestCase(unittest.TestCase):
    """
    Base test
    """
    # could create the md instance here?
    pass


def suite():
    # NTS what order should these go in?

    # add all glossay link tests
    glossarySuite = unittest.makeSuite(GlossaryLinkTest, 'test') # order of tests by cmp()
    # add all panel tests
    panelSuite = unittest.makeSuite(PanelTest, 'test')

    allSuites = unittest.TestSuite((glossarySuite, panelSuite))

    # NTS to add each tag's tests individually
    # suite.addTest(GlossaryLinkTest('test_match_true'))
    # suite.addTest(GlossaryLinkTest('test_match_false'))
    return allSuites



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)



