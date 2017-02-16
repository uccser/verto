import markdown
from unittest.mock import Mock
from collections import defaultdict

from kordac.KordacExtension import KordacExtension
from kordac.processors.ImageBlockProcessor import ImageBlockProcessor
from kordac.tests.BaseTestCase import BaseTestCase

class ImageTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'image'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)
        self.ext.required_files = defaultdict(set)

    def test_internal_image(self):
        test_string = self.read_test_file('internal_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('internal_image_expected')

        self.assertEqual(expected_string, converted_test_string)

    def test_external_image(self):
        test_string = self.read_test_file('external_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('external_image_expected')

        self.assertEqual(expected_string, converted_test_string)

    def test_default_image(self):
        test_string = self.read_test_file('default_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('default_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_images(self):
        test_string = self.read_test_file('contains_multiple_images')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_images_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_no_image(self):
        test_string = self.read_test_file('no_image')
        self.assertFalse(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_image(self):
        test_string = self.read_test_file('text_contains_the_word_image')
        self.assertFalse(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('text_contains_the_word_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_image(self):
        test_string = self.read_test_file('contains_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_image_and_text_contains_word_image(self):
        test_string = self.read_test_file('contains_image_and_text_contains_word_image')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_image_and_text_contains_word_image_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_hover_text(self):
        test_string = self.read_test_file('contains_hover_text')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_hover_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_caption_link(self):
        test_string = self.read_test_file('contains_caption_link')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_caption_link_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_alt(self):
        test_string = self.read_test_file('contains_alt')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_alt_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_caption(self):
        test_string = self.read_test_file('contains_caption')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_caption_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_source(self):
        test_string = self.read_test_file('contains_source')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_source_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_align_left(self):
        test_string = self.read_test_file('align_left')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('align_left_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_align_right(self):
        test_string = self.read_test_file('align_right')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('align_right_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_align_center(self):
        test_string = self.read_test_file('align_center')
        self.assertTrue(ImageBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg=''.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('align_center_expected')
        self.assertEqual(expected_string, converted_test_string)
