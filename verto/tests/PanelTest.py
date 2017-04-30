import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.tests.ProcessorTest import ProcessorTest

class PanelTest(ProcessorTest):
    '''The panel processor inherits from the generic container.
    The tests contained here test that arguments and the output
    (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic container to test that the matches are
        occuring appropriately and configure the asset directory.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'panel'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.block_processor = GenericContainerBlockProcessor(self.processor_name, self.ext, Mock())

    def test_parses_blank(self):
        '''Tests that a blank panel is processed with empty content.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]),test_string)

    def test_parses_no_blank_lines_single_paragraph(self):
        '''Tests that a block of text as content is added to the panel.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_expanded_panel(self):
        '''Tests that the expanded argument works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_always_expanded_panel(self):
        '''Tests the the always expanded argument works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        '''Tests that multiple blocks of text as the content are
        processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, False, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_panels(self):
        '''Tests that multiple panels are processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_panels.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True, True, False, True, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_panels_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inner_panel(self):
        '''Tests that panels can contain other panels.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_inner_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inner_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_start_tag(self):
        '''Tests that TagNotMatchedErrors are thown when an end tag is
        encountered alone.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_start_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_end_tag(self):
        '''Tests that TagNotMatchedErrors are thown when an end tag is
        encountered alone.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_tag_inner(self):
        '''Tests that if inner tags are missing that the
        TagNotMatchedErrors are thown.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_tag_inner.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_contains_inner_image(self):
        '''Tests that other processors within a panel
        still renders correctly.
        '''
        verto_extension = VertoExtension([self.processor_name, 'image'], {})
        test_string = self.read_test_file(self.processor_name, 'contains_inner_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inner_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_panel_in_numbered_list(self):
        '''Tests that panels and containers work within numbered lists.
        '''
        test_string = self.read_test_file(self.processor_name, 'panel_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'panel_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_panel_only_in_numbered_list(self):
        '''Tests that panels and containers work within numbered lists.
        '''
        test_string = self.read_test_file(self.processor_name, 'panel_only_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'panel_only_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''Example of the common usecase.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''Example of overriding the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
