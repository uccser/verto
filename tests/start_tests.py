import unittest
from collections import defaultdict

from tests.glossary_tests import *
from tests.panel_tests import PanelTest
from tests.comment_tests import CommentTest
from tests.heading_tests import *
from tests.image_tests import *
from tests.video_tests import *
from tests.interactive_tests import *


def suite():
    # NTS what order should these go in?
    allSuites = unittest.TestSuite((
        unittest.makeSuite(GlossaryLinkTest), # order of tests by cmp()
        unittest.makeSuite(PanelTest),
        unittest.makeSuite(CommentTest),
        unittest.makeSuite(HeadingTest),
        unittest.makeSuite(ImageTest),
        unittest.makeSuite(VideoTest),
        unittest.makeSuite(InteractiveTest)
    ))

    return allSuites


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
