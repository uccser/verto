import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.BlockquoteBlockProcessor import BlockquoteBlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.errors.BlockquoteMissingFooterError import BlockquoteMissingFooterError
from verto.errors.StyleError import StyleError
from verto.tests.ProcessorTest import ProcessorTest


class BlockquoteTest(ProcessorTest):
    '''The blockquote processor inherits from the generic container.
    The tests contained here test that arguments and the output
    (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic container to test that the matches are
        occuring appropriately and configure the asset directory.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'blockquote'
        self.ext = Mock()
        self.ext.jinja_templates = {
            self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)
        }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.block_processor = BlockquoteBlockProcessor(self.ext, Mock())

    def test_no_footer(self):
        '''Tests that a blockquote without a footer
        '''
        test_string = self.read_test_file(self.processor_name, 'no_footer.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_footer_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer(self):
        '''Tests that a blockquote with a footer
        '''
        test_string = self.read_test_file(self.processor_name, 'footer.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_no_content(self):
        '''Tests that a blockquote with a footer but no content raises an error
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_no_content.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_footer_with_markdown_formatting(self):
        '''Tests that a blockquote with a footer with Markdown formatting (bold and italics)
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_markdown_formatting.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_markdown_formatting_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_with_link(self):
        '''Tests that a blockquote with a footer with Markdown link
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_link_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_with_multiple_dash_prefix(self):
        '''Tests that a blockquote with a footer with multiple dashes prefix
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_multiple_dash_prefix.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_multiple_dash_prefix_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_missing_content(self):
        '''Tests that correct error raised when footer is missing
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_missing_content.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(BlockquoteMissingFooterError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_footer_invalid_prefix(self):
        '''Tests that correct error raised when footer prefix is invalid
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_invalid_prefix.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(BlockquoteMissingFooterError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_parses_blank(self):
        '''Tests that a blank panel is processed with empty content.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''Example of the common usecase.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
