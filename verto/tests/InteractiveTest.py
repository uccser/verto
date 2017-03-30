import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from verto.tests.ProcessorTest import ProcessorTest

class InteractiveTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'interactive'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name), 'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')}
        self.ext.required_files = defaultdict(set)

    def test_doc_example_in_page(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_in_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_in_page_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_whole_page(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_whole_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_whole_page_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_iframe(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_iframe_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_iframe_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
