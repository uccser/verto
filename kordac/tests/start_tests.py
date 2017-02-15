import unittest
from collections import defaultdict

from kordac.tests.GlossaryLinkTest import GlossaryLinkTest
from kordac.tests.PanelTest import PanelTest
from kordac.tests.CommentTest import CommentTest
from kordac.tests.HeadingTest import HeadingTest
from kordac.tests.ImageTest import ImageTest
from kordac.tests.VideoTest import VideoTest
from kordac.tests.InteractiveTest import InteractiveTest
from kordac.tests.ButtonLinkTest import ButtonLinkTest
from kordac.tests.BoxedTextTest import BoxedTextTest
from kordac.tests.SaveTitleTest import SaveTitleTest
from kordac.tests.RemoveTitleTest import RemoveTitleTest

def suite():
    # NTS what order should these go in?
    allSuites = unittest.TestSuite((
        unittest.makeSuite(SaveTitleTest),
        unittest.makeSuite(RemoveTitleTest),
        # unittest.makeSuite(GlossaryLinkTest), # order of tests by cmp()
        unittest.makeSuite(PanelTest),
        unittest.makeSuite(CommentTest),
        unittest.makeSuite(HeadingTest),
        unittest.makeSuite(ImageTest),
        # unittest.makeSuite(VideoTest),
        # unittest.makeSuite(InteractiveTest),
        # unittest.makeSuite(ButtonLinkTest)
        unittest.makeSuite(BoxedTextTest)
    ))

    return allSuites


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
