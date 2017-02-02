import markdown
from unittest.mock import Mock

from Kordac import Kordac
from processors.ButtonPreprocessor import ButtonPreprocessor
from tests.BaseTestCase import BaseTestCase


class ButtonTest(BaseTestCase):
    """
    """

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'button'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)
        self.ext.html_templates = {self.tag_name: BaseTestCase.loadHTMLTemplate(self, self.tag_name)}

    def test_on_button(self):
        pass

    def test_contains_button(self):
        test_string = self.read_test_file('contains_button')
        self.assertTrue(ButtonPreprocessor(self.ext, self.md.parser).test(test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('contains_button_expected')
        print('CONVERTED')
        print(converted_test_string)
        # print('EXPECTED')
        # print(expected_string)
        self.assertEqual(expected_string, converted_test_string)


