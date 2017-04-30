import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.StylePreprocessor import StylePreprocessor
from verto.errors.StyleError import StyleError
from verto.tests.ProcessorTest import ProcessorTest

class StyleTest(ProcessorTest):
    '''Checks that failures are raised correctly.
    '''

    def __init__(self, *args, **kwargs):
        '''Setup name for asset file location.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'style'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_doc_example_block_whitespace(self):
        '''Test before an after a block.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_whitespace_1(self):
        '''Test no whitespace before an after content in
        a block container.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_1.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_whitespace_2(self):
        '''Test no whitespace before a block tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_2.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_whitespace_3(self):
        '''Test no whitespace after a block tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_whitespace_3.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_solitary(self):
        '''Test extra text after a tag that should be
        solitary.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_solitary.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_solitary_1(self):
        '''Test extra text before a tag that should be
        solitary.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_solitary_1.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_valid(self):
        '''A valid example of using container tags.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_valid.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_valid_in_list(self):
        '''A valid example of using container tags.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_valid_in_list.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])

    def test_doc_example_block_error_in_list(self):
        '''A valid example of using container tags.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_block_error_in_list.md')
        with self.assertRaises(StyleError):
            converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
