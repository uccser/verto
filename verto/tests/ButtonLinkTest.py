import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.tests.ProcessorTest import ProcessorTest


class ButtonLinkTest(ProcessorTest):
    '''The ButtonLink processor inherits from the generic tag procesor.
    The tests contained here test that arguments and the output
    (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic tag to test that the matches are occuring appropriately.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'button-link'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name), 'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')}
        self.block_processor = GenericTagBlockProcessor(self.processor_name, self.ext, Mock())

    def test_no_button(self):
        '''Tests that the text containing the processor name is not matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False] * 7, [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_button(self):
        '''Tests that the most generic case of a single match is found with generic content contained within.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_missing_button(self):
        '''Tests that paritial matches do not occur.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_end_brace.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'missing_end_brace_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_buttons(self):
        '''Tests that multiple buttons within a document are matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False, True, False, False, True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_buttons_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_file_link_button(self):
        '''Tests that the file argument works are expected, internally linking to a file.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_file_link_button.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

        expected_string = self.read_test_file(self.processor_name, 'contains_file_link_button_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

# link text file
    def test_custom_arguments_link_false(self):
        '''Tests to ensure that button link tag is rendered correctly when link argument is required.
        '''
        settings = {
            'processor_argument_overrides': {
                'button-link': {
                    'link': False,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'link_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'link_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_text_false(self):
        '''Tests to ensure that button link tag is rendered correctly when text argument is false.
        '''
        settings = {
            'processor_argument_overrides': {
                'button-link': {
                    'text': False,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'text_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'text_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_file_true(self):
        '''Tests to ensure that button link tag is rendered correctly when file argument is true.
        '''
        settings = {
            'processor_argument_overrides': {
                'button-link': {
                    'file': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'file_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'file_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_text_false_file_true(self):
        '''Tests to ensure that button link tag is rendered correctly when text argument is false and file argument is true.
        '''
        settings = {
            'processor_argument_overrides': {
                'button-link': {
                    'file': True,
                    'text': False,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'text_false_file_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'text_false_file_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_file_true_not_provided(self):
        '''Tests to ensure that error is raised when file argument is required and not given.
        '''
        settings = {
            'processor_argument_overrides': {
                'button-link': {
                    'file': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'file_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''Tests that the most generic case of a single match is found
        with generic content contained within.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_file(self):
        '''Tests that file argument for internal files works as
        expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_file_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_file_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''Tests and shows example of overriding the html of the
        processor.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
