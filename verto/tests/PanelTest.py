import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.PanelBlockProcessor import PanelBlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.errors.PanelMissingTitleError import PanelMissingTitleError
from verto.errors.PanelMissingSubtitleError import PanelMissingSubtitleError
from verto.errors.StyleError import StyleError
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
        self.block_processor = PanelBlockProcessor(self.ext, Mock())

    def test_heading_no_subtitle(self):
        '''Tests that a heading is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_no_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_no_subtitle_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_with_punctuation(self):
        '''Tests that a heading is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_with_punctuation.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_with_punctuation_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_subtitle_false(self):
        '''Tests that a heading is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_subtitle_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_subtitle_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_subtitle_false_h2_heading_in_panel(self):
        '''Tests that a heading is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_subtitle_false_h2_heading_in_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_subtitle_false_h2_heading_in_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_with_subtitle(self):
        '''Tests that both a heading and subtitle is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_with_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_with_subtitle_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_with_subtitle_with_punctuation(self):
        '''Tests that both a heading and subtitle is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_with_subtitle_with_punctuation.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_with_subtitle_with_punctuation_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_heading_with_subtitle_h2_heading_in_panel(self):
        '''Tests that both a heading and subtitle is parsed correctly
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_with_subtitle_h2_heading_in_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_with_subtitle_h2_heading_in_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_missing_heading_with_subtitle(self):
        '''Tests that correct error raised when heading is missing
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_heading_with_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingTitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_heading_missing_subtitle(self):
        '''Tests that correct error raised when subtitle is missing
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_missing_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingSubtitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_heading_invalid_subtitle_argument(self):
        '''Tests that correct error raised when incorrect valude givent for subtitle argument
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_invalid_subtitle_argument.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_heading_missing_subtitle(self):
        '''Tests that correct error raised when heading and subtitle are missing
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_heading_missing_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingTitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_incorrect_heading_no_subtitle(self):
        '''Tests that correct error raised when heading is incorrect
        '''
        test_string = self.read_test_file(self.processor_name, 'incorrect_heading_no_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingTitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_incorrect_heading_with_subtitle(self):
        '''Tests that correct error raised when heading is incorrect
        '''
        test_string = self.read_test_file(self.processor_name, 'incorrect_heading_with_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingTitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_heading_incorrect_subtitle(self):
        '''Tests that correct error raised when subtitle is incorrect
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_incorrect_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingSubtitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_heading_subtitle_no_whitespace(self):
        '''Tests that heading and subtitle render correctly when no
        whitespace is given between heading level and text.
        '''
        test_string = self.read_test_file(self.processor_name, 'heading_subtitle_no_whitespace.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'heading_subtitle_no_whitespace_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank(self):
        '''Tests that a blank panel is processed with empty content.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_parses_no_blank_lines_single_paragraph(self):
        '''Tests that a block of text as content is added to the panel.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_no_blank_lines_single_paragraph_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_expanded_panel(self):
        '''Tests that the expanded argument works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_always_expanded_panel(self):
        '''Tests the the always expanded argument works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_always_expanded_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_parses_blank_lines_multiple_paragraphs(self):
        '''Tests that multiple blocks of text as the content are
        processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, False, False, False, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'parses_blank_lines_multiple_paragraphs_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_panels(self):
        '''Tests that multiple panels are processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_panels.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True, True, False, False, False, True, True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_panels_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inner_panel(self):
        '''Tests that panels can contain other panels.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_inner_panel.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True, False, False, False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inner_panel_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_inner_panel_missing_subtitle(self):
        '''Tests that panels can contain other panels and subtitles are rendered correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_inner_panel_missing_subtitle.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True, False, False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(PanelMissingSubtitleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_start_tag(self):
        '''Tests that TagNotMatchedErrors are thown when an end tag is
        encountered alone.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_start_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_end_tag(self):
        '''Tests that TagNotMatchedErrors are thown when an end tag is
        encountered alone.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_tag_inner(self):
        '''Tests that if inner tags are missing that the
        TagNotMatchedErrors are thown.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_tag_inner.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_contains_inner_image(self):
        '''Tests that other processors within a panel still renders correctly.'''
        verto_extension = VertoExtension([self.processor_name, 'image-container'], {})
        test_string = self.read_test_file(self.processor_name, 'contains_inner_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, False, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_inner_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_panel_in_numbered_list(self):
        '''Tests that panels and containers work within numbered lists.
        '''
        test_string = self.read_test_file(self.processor_name, 'panel_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False, False, False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'panel_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_panel_only_in_numbered_list(self):
        '''Tests that panels and containers work within numbered lists.
        '''
        test_string = self.read_test_file(self.processor_name, 'panel_only_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False, False, False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'panel_only_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_panel_block_missing_whitespace(self):
        '''Tests that panels and containers work within numbered lists.
        '''
        test_string = self.read_test_file(self.processor_name, 'panel_block_missing_whitespace.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(StyleError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_custom_arguments_type_false(self):
        '''Tests to ensure that panel tag is rendered correctly when type argument is not required.
        '''
        custom_argument_rules = {
            "panel": {
                "type": False
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'type_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'type_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_subtitle_true(self):
        '''Tests to ensure that panel tag is rendered correctly when subtitle argument is required.
        '''
        custom_argument_rules = {
            "panel": {
                "subtitle": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'subtitle_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'subtitle_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_expanded_true(self):
        '''Tests to ensure that panel tag is rendered correctly when expanded argument is required.
        '''
        custom_argument_rules = {
            "panel": {
                "expanded": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'expanded_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'expanded_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_subtitle_true_not_provided(self):
        '''Tests to ensure that correct error is raised when subtitle is required and not provided.
        '''
        custom_argument_rules = {
            "panel": {
                "subtitle": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'subtitle_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''Example of the common usecase.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''Example of overriding the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
