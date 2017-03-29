import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from kordac.processors.errors.TagNotMatchedError import TagNotMatchedError
from kordac.tests.ProcessorTest import ProcessorTest

class PanelTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'panel'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.block_processor = GenericContainerBlockProcessor(self.processor_name, self.ext, Mock())

    def test_parses_blank(self):
        test_string = self.read_test_file(self.processor_name, 'parses_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_blank_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_no_blank_lines_single_paragraph(self):
        test_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_expanded_panel(self):
        test_string = self.read_test_file(self.processor_name, 'parses_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_always_expanded_panel(self):
        test_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        test_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, False, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_panels(self):
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_panels.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True, True, False, True, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_panels_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inner_panel(self):
        test_string = self.read_test_file(self.processor_name, 'contains_inner_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inner_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_start_tag(self):
        test_string = self.read_test_file(self.processor_name, 'missing_start_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    def test_missing_end_tag(self):
        test_string = self.read_test_file(self.processor_name, 'missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    def test_missing_tag_inner(self):
        test_string = self.read_test_file(self.processor_name, 'missing_tag_inner.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
