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
        pass

    def test_parses_blank_lines_multiple_paragraphs(self):
        pass

    def test_parses_no_blank_self(self):
        pass

    def test_parses_external_link(self):
        test_string = self.read_test_file('parses_external_link')
        self.assertTrue(PanelBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[Kordac()])
        expected_string = self.read_expected_output_file('parses_external_link')
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_glossary_link(self):
        pass

    def test_parses_video_link(self):
        pass

    def test_parses_codeblock(self):
        pass

    def test_parses_pictures(self):
        pass

    def test_parses_mathblocks(self):
        pass

    def test_parses_comments(self):
        pass
