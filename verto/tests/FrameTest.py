import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.processors.errors.ArgumentMissingError import ArgumentMissingError
from verto.tests.ProcessorTest import ProcessorTest

class FrameTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'iframe'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.block_processor = GenericTagBlockProcessor(self.processor_name, self.ext, Mock())

    def test_example_no_link(self):
        test_string = self.read_test_file(self.processor_name, 'example_no_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        with self.assertRaises(ArgumentMissingError):
            markdown.markdown(test_string, extensions=[self.verto_extension])

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
