import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.StylePreprocessor import StylePreprocessor
from kordac.processors.errors.StyleError import StyleError
from kordac.tests.ProcessorTest import ProcessorTest

class StyleTest(ProcessorTest):
    """
    Inline = single line comment .e.g. {comment hello you look lovely today}
    """

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'style'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_doc_example_block_whitespace(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_whitespace_1(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_1.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_whitespace_2(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_2.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_whitespace_3(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_3.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_solitary(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_solitary.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_solitary_1(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_solitary_1.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

    def test_doc_example_block_valid(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_valid.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
