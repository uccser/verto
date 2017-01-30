import markdown
from unittest.mock import Mock
from collections import defaultdict

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
        self.ext.required_files = defaultdict(set)


    def test_match_false(self):
        """
        Test no match found in string where there is no image
        """
        test_string = self.read_test_file('no_image')
        self.assertFalse(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        test_string = self.read_test_file('text_contains_the_word_image')
        self.assertFalse(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

    def test_match_true(self):
        """
        Test finds matches in strings where there is an image included
        """
        test_string = self.read_test_file('contains_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        test_string = self.read_test_file('contains_multiple_images')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        test_string = self.read_test_file('contains_image_and_text_contains_word_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        test_string = self.read_test_file('image_in_panel')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

    def test_unchanged(self):
        """
        Test text with no matches is unchanged
        """
        test_string = self.read_test_file('no_image')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('no_image_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('text_contains_the_word_image')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('text_contains_the_word_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_image_link_converted_to_django_tag(self):
        """
        Test text with image is converted to django image syntax
        """
        test_string = self.read_test_file('contains_image')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_image_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_multiple_images')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_multiple_images_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('contains_image_and_text_contains_word_image')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('contains_image_and_text_contains_word_image_expected')
        self.assertEqual(expected_string, converted_test_string)

        test_string = self.read_test_file('image_in_panel')
        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_test_file('image_in_panel_expected')
        self.assertEqual(expected_string, converted_test_string)

