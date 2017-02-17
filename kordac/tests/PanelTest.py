import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.PanelBlockProcessor import PanelBlockProcessor
from kordac.processors.errors.TagNotMatchedError import TagNotMatchedError
from kordac.tests.BaseTestCase import BaseTestCase

class PanelTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'panel'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_info = BaseTestCase.loadProcessorInfo(self)

    def test_parses_blank(self):
        test_string = self.read_test_file('parses_blank')
        blocks = self.to_blocks(test_string)

        self.assertTrue(all(PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('parses_blank_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_no_blank_lines_single_paragraph(self):
        test_string = self.read_test_file('parses_no_blank_lines_single_paragraph')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('parses_no_blank_lines_single_paragraph_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_expanded_panel(self):
        test_string = self.read_test_file('parses_expanded_panel')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('parses_expanded_panel_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_always_expanded_panel(self):
        test_string = self.read_test_file('parses_always_expanded_panel')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('parses_always_expanded_panel_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        test_string = self.read_test_file('parses_blank_lines_multiple_paragraphs')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('parses_blank_lines_multiple_paragraphs_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_panels(self):
        test_string = self.read_test_file('contains_multiple_panels')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_multiple_panels_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inner_panel(self):
        test_string = self.read_test_file('contains_inner_panel')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_expected_output_file('contains_inner_panel_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_start_tag(self):
        test_string = self.read_test_file('missing_start_tag')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    def test_missing_end_tag(self):
        test_string = self.read_test_file('missing_end_tag')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    def test_missing_tag_inner(self):
        test_string = self.read_test_file('missing_tag_inner')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (PanelBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)
