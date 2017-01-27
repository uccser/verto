import unittest
import markdown

from Kordac import Kordac
from processors.ImageBlockProcessor import ImageBlockProcessor
from tests.BaseTestCase import BaseTestCase

class ImageTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'image'
        self.ext = Mock()
        self.ext.html_templates = {self.tag_name: BaseTestCase.loadHTMLTemplate(self, self.tag_name)}
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)


    def test_match_false(self):
        """
        hey look! I'm a docstring!
        """
        test_string = self.read_test_file('no_image')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))

        test_string = self.read_test_file('text_contains_the_word_image')
        self.assertFalse(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))


    def test_match_true(self):
        """
        this needs  a good docstring
        """
        test_string = self.read_test_file('contains_image')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))

        test_string = self.read_test_file('contains_multiple_images')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))

        test_string = self.read_test_file('contains_image_and_text_contains_word_image')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))

        test_string = self.read_test_file('image_in_panel')
        self.assertTrue(CommentPreprocessor(self.ext, self.md.parser).test(test_string), msg=''.format(test_string))

