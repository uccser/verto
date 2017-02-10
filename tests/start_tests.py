import unittest
from collections import defaultdict

from tests.GlossaryLinkTest import GlossaryLinkTest
from tests.PanelTest import PanelTest
from tests.CommentPreTest import CommentPreTest
from tests.CommentBlockTest import CommentBlockTest
from tests.HeadingTest import HeadingTest
from tests.ImageTest import ImageTest
from tests.VideoTest import VideoTest
from tests.InteractiveTest import InteractiveTest
from tests.ButtonLinkTest import ButtonLinkTest


def suite():
    # NTS what order should these go in?
    allSuites = unittest.TestSuite((
        # unittest.makeSuite(GlossaryLinkTest), # order of tests by cmp()
        # unittest.makeSuite(PanelTest),
        unittest.makeSuite(CommentPreTest),
        unittest.makeSuite(CommentBlockTest),
        unittest.makeSuite(HeadingTest),
        unittest.makeSuite(ImageTest),
        unittest.makeSuite(VideoTest),
        unittest.makeSuite(InteractiveTest),
        unittest.makeSuite(ButtonLinkTest)
    ))

    return allSuites


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
