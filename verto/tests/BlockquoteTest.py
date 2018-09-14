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
        '''Tests that a blockquote without a footer renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_footer.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_footer_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer(self):
        '''Tests that a blockquote with a footer renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_false(self):
        '''Tests that a blockquote with footer argument set to false renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_no_content(self):
        '''Tests that a blockquote with a footer but no content raises an error renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_no_content.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_footer_with_markdown_formatting(self):
        '''Tests that a blockquote with a footer with Markdown formatting (bold and italics) renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_markdown_formatting.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_markdown_formatting_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_with_link(self):
        '''Tests that a blockquote with a footer with Markdown link renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_link_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_with_multiple_dash_prefix(self):
        '''Tests that a blockquote with a footer with multiple dashes prefix renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_with_multiple_dash_prefix.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'footer_with_multiple_dash_prefix_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_footer_missing_content(self):
        '''Tests that correct error raised when footer is missing renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_missing_content.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(BlockquoteMissingFooterError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_footer_invalid_prefix(self):
        '''Tests that correct error raised when footer prefix is invalid renders correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'footer_invalid_prefix.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(BlockquoteMissingFooterError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_parses_blank(self):
        '''Tests that a blank blockquotes is processed with empty content.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)


    def test_multiple_blockquotes(self):
        '''Tests that multiple blockquotes are processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_blockquotes.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, True, False, True, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_blockquotes_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_start_tag(self):
        '''Tests that a TagNotMatchedError is thrown when a start tag is missing.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_start_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_end_tag(self):
        '''Tests that a TagNotMatchedError is thrown when an end tag is missing.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_custom_arguments_source_true(self):
        '''Tests to ensure that blockquote tag is rendered correctly when source argument is required.
        '''
        custom_argument_rules = {
            "blockquote": {
                "source": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'source_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'source_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_source_true_missing_argument(self):
        '''Tests to ensure that blockquote tag raises errors when source argument is required and not given.
        '''
        custom_argument_rules = {
            "blockquote": {
                "source": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'source_true_missing_argument.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    def test_custom_arguments_alignment_true(self):
        '''Tests to ensure that blockquote tag is rendered correctly when alignment argument is required.
        '''
        custom_argument_rules = {
            "blockquote": {
                "alignment": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'alignment_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'alignment_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_alignment_true_missing_argument(self):
        '''Tests to ensure that blockquote tag raises errors when alignment argument is required and not given.
        '''
        custom_argument_rules = {
            "blockquote": {
                "alignment": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'alignment_true_missing_argument.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

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
