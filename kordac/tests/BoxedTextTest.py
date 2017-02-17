import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.BoxedTextBlockProcessor import BoxedTextBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest


class BoxedTextTest(ProcessorTest):
    """
    """

    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'boxed-text'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_no_boxed_text(self):
        test_string = self.read_test_file(self.processor_name, 'no_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(all(BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) == False for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_single_boxed_text(self):
        test_string = self.read_test_file(self.processor_name, 'single_boxed_text.md')
        blocks = self.to_blocks(test_string)

        processor = BoxedTextBlockProcessor(self.ext, self.md.parser)
        self.assertTrue(True in (processor.test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'single_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_boxed_text(self):
        test_string = self.read_test_file(self.processor_name, 'indented_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'indented_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_boxed_text(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_recursive_boxed_text(self):
        test_string = self.read_test_file(self.processor_name, 'recursive_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'recursive_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertTrue(True in (BoxedTextBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
