import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.BoxedTextBlockProcessor import BoxedTextBlockProcessor
from tests.BaseTestCase import BaseTestCase


class BoxedTextTest(BaseTestCase):
    """
    """

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'boxed-text'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)
        self.ext.html_templates = {self.tag_name: BaseTestCase.loadHTMLTemplate(self, self.tag_name)}
        # TODO: Proper Setup with template for jinja

    def test_no_boxed_text(self):
        test_string = self.read_test_file('no_boxed_text')
        self.assertTrue(BoxedTextBlockProcessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_single_boxed_text(self):
        test_string = self.read_test_file('single_boxed_text')
        self.assertTrue(BoxedTextBlockProcessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('single_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_boxed_text(self):
        test_string = self.read_test_file('multiple_boxed_text')
        self.assertTrue(BoxedTextBlockProcessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_boxed_text(self):
        test_string = self.read_test_file('indented_boxed_text')
        self.assertTrue(BoxedTextBlockProcessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('indented_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_boxed_text_with_link(self):
        pass
