import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.tests.ProcessorTest import ProcessorTest


class TableOfContentsTest(ProcessorTest):
    '''The table-of-contents processor inherits from the generic
    tag procesor.  The tests contained here test that arguments
    and the output (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic tag to test that the matches are
        occuring appropriately.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'table-of-contents'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.block_processor = GenericTagBlockProcessor(self.processor_name, self.ext, Mock())

    # ~
    # Doc Tests
    # ~

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
