import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.ButtonLinkBlockProcessor import ButtonLinkBlockProcessor
from kordac.tests.BaseTestCase import BaseTestCase


class ButtonLinkTest(BaseTestCase):
    """
    """

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'button-link'
        self.ext = Mock()
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}

    def test_no_button(self):
        test_string = self.read_test_file('no_button')
        blocks = self.to_blocks(test_string)

        self.assertFalse(any(ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_button_expected')
        self.assertEqual(expected_string, converted_test_string)

    # def test_contains_button(self):
    #     test_string = self.read_test_file('contains_button')
    #     blocks = self.to_blocks(test_string)
    #
    #     self.assertTrue(all(ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))
    #
    #     converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
    #     expected_string = self.read_expected_output_file('contains_button_expected')
    #     self.assertEqual(expected_string, converted_test_string)
    #
    # def test_contains_button(self):
    #     test_string = self.read_test_file('missing_end_brace')
    #     blocks = self.to_blocks(test_string)
    #
    #     self.assertTrue(all(ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))
    #
    #     converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
    #     expected_string = self.read_expected_output_file('missing_end_brace_expected')
    #     self.assertEqual(expected_string, converted_test_string)
    #
    # def test_contains_multiple_buttons_expected(self):
    #     test_string = self.read_test_file('contains_multiple_buttons')
    #     blocks = self.to_blocks(test_string)
    #
    #     self.assertTrue(all(ButtonLinkBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))
    #
    #     converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
    #     expected_string = self.read_expected_output_file('contains_multiple_buttons_expected')
    #     self.assertEqual(expected_string, converted_test_string)
