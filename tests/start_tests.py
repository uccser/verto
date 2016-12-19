import unittest
import markdown
from markdown.extensions import Extension
from collections import defaultdict

from tests.glossary_tests import *
from tests.panel_tests import *
from tests.comment_tests import *
from tests.heading_tests import *
from tests.image_tests import *
from tests.video_tests import *
from tests.interactive_tests import *


class BaseTestCase(unittest.TestCase):
    """
    Base test
    """
    # could create the md instance here?
    pass


def suite():
    # NTS what order should these go in?
    allSuites = unittest.TestSuite((
        unittest.makeSuite(GlossaryLinkTest, 'test'), # order of tests by cmp()
        unittest.makeSuite(PanelTest, 'test'),
        unittest.makeSuite(CommentTest, 'test'),
        unittest.makeSuite(HeadingTest, 'test'),
        unittest.makeSuite(ImageTest, 'test'),
        unittest.makeSuite(VideoTest, 'test'),
        unittest.makeSuite(InteractiveTest, 'test')
        ))

    return allSuites



if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)



