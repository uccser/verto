import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentDefinitionError import ArgumentDefinitionError
from verto.tests.ProcessorTest import ProcessorTest


class FrameTest(ProcessorTest):
    '''The iframe processor inherits from the generic tag procesor.
    The tests contained here test that arguments and the output
    (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic tag to test that the matches are
        occuring appropriately.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'iframe'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.block_processor = GenericTagBlockProcessor(self.processor_name, self.ext, Mock())

    def test_example_no_link(self):
        '''Tests that the text containing the processor name is
        not matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_no_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        with self.assertRaises(ArgumentMissingError):
            markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_example_single_quote_argument_error(self):
        '''Tests that single quotes as an argument raise the
        ArgumentDefinitionError. This is a test that affects all
        processors of the generic type (and any that use the
        parse_argument function in utils).
        '''
        test_string = self.read_test_file(self.processor_name, 'example_single_quote_argument_error.md')

        with self.assertRaises(ArgumentDefinitionError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_custom_argument_rules_link_false(self):
        '''Tests to ensure that iframe tag is rendered correctly when link argument is not required.
        '''
        custom_argument_rules = {
            "iframe": {
                "link": False
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'link_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'link_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''A generic example of common usage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''A example showing how to override the html template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
