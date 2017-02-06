import unittest
from collections import defaultdict

from kordac.tests.GlossaryLinkTest import GlossaryLinkTest
from kordac.tests.PanelTest import PanelTest
from kordac.tests.CommentPreTest import CommentPreTest
from kordac.tests.CommentBlockTest import CommentBlockTest
from kordac.tests.HeadingTest import HeadingTest
from kordac.tests.ImageTest import ImageTest
from kordac.tests.VideoTest import VideoTest
from kordac.tests.InteractiveTest import InteractiveTest
from kordac.tests.ButtonTest import ButtonTest


def suite():
    # NTS what order should these go in?
    allSuites = unittest.TestSuite((
        # unittest.makeSuite(GlossaryLinkTest), # order of tests by cmp()
        unittest.makeSuite(PanelTest),
        # unittest.makeSuite(CommentPreTest),
        # unittest.makeSuite(CommentBlockTest),
        # unittest.makeSuite(HeadingTest),
        # unittest.makeSuite(ImageTest),
        # unittest.makeSuite(VideoTest),
        # unittest.makeSuite(InteractiveTest),
        # unittest.makeSuite(ButtonTest)
    ))

    return allSuites


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
