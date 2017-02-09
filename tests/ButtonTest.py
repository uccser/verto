import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.ButtonPreprocessor import ButtonPreprocessor
from tests.BaseTestCase import BaseTestCase


class ButtonTest(BaseTestCase):
    """
    """

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'button'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)
        self.ext.jinja_templates = {self.tag_name: BaseTestCase.loadJinjaTemplate(self, self.tag_name)}

    def test_no_button(self):
        test_string = self.read_test_file('no_button')
        self.assertFalse(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_button_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_button(self):
        test_string = self.read_test_file('contains_button')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_button_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_buttons_expected(self):
        test_string = self.read_test_file('contains_multiple_buttons')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_buttons_expected')
        self.assertEqual(expected_string, converted_test_string)
