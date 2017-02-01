import markdown
from unittest.mock import Mock

from Kordac import Kordac
from processors.PanelBlockProcessor import PanelBlockProcessor
from tests.BaseTestCase import BaseTestCase

class PanelTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'panel'
        self.ext = Mock()
        self.ext.html_templates = {self.tag_name: BaseTestCase.loadHTMLTemplate(self, self.tag_name)}
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)

    def test_parses_no_blank_lines_single_paragraph(self):
        test_string = self.read_test_file('parses_no_blank_lines_single_paragraph')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_no_blank_lines_single_paragraph_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        test_string = self.read_test_file('parses_no_blank_lines_multiple_paragraphs')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_no_blank_lines_multiple_paragraphs_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank(self):
        test_string = self.read_test_file('parses_blank')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_blank_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_panels(self):
        test_string = self.read_test_file('test_contains_multiple_panels')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('test_contains_multiple_panels_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_single_line(self):
        test_string = self.read_test_file('single_line')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('single_line_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_start_tag(self):
        # TODO: should error
        test_string = self.read_test_file('missing_start_tag')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('missing_start_tag_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_end_tag(self):
        # TODO: check functionality
        test_string = self.read_test_file('missing_end_tag')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('missing_end_tag_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_external_link(self):
        test_string = self.read_test_file('parses_external_link')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_external_link_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_glossary_link(self):
        test_string = self.read_test_file('parses_glossary_link')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_glossary_link_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_video_link(self):
        test_string = self.read_test_file('parses_video_link')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_video_link_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_codeblock(self):
        test_string = self.read_test_file('parses_codeblock')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_codeblock_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_pictures(self):
        test_string = self.read_test_file('parses_pictures')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_pictures_expected')
        self.assertEqual(expected_string, converted_test_string))

    def test_parses_mathblocks(self):
        test_string = self.read_test_file('parses_mathblock')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_mathblock_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_comments_pre(self):
        test_string = self.read_test_file('parses_comments')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_comments_pre_expected')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_comments(self):
        test_string = self.read_test_file('parses_comments')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_comments')
        self.assertEqual(expected_string, converted_test_string)
