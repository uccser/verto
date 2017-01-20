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
    """A base test class for individual test classes"""
    
    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class
        
        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.test_file_path = 'tests/assets/{tag_name}/{filename}.txt'
        self.maxDiff = 640  # Set to None for full output of all test failures

    def read_test_file(self, filename):
        """Returns a string for a given file
        
        This function reads a file from a given filename in UTF-8 encoding.
        """
        file_path = self.test_file_path.format(tag_name=self.tag_name, filename=filename)
        file_object = open(file_path, encoding="utf-8")
        return file_object.read()
        
    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])

    def tearDown(self):
        self.md = None


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
