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
        self.ext.jinja_templates = {self.tag_name: BaseTestCase.loadJinjaTemplate(self, self.tag_name)}

    def test_no_boxed_text(self):
        test_string = self.read_test_file('no_boxed_text')
        blocks = self.to_blocks(test_string)

        self.assertTrue(all(BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) == False for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('no_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_single_boxed_text(self):
        test_string = self.read_test_file('single_boxed_text')
        blocks = self.to_blocks(test_string)

        processor = BoxedTextBlockProcessor(self.ext, self.md.parser)
        self.assertTrue(True in (processor.test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('single_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_boxed_text(self):
        test_string = self.read_test_file('indented_boxed_text')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('indented_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_boxed_text(self):
        test_string = self.read_test_file('multiple_boxed_text')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('multiple_boxed_text_expected')
        self.assertEqual(expected_string, converted_test_string)
