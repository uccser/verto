import markdown

from verto.VertoExtension import VertoExtension
from verto.processors.ScratchTreeprocessor import ScratchImageMetaData
from verto.tests.ProcessorTest import ProcessorTest


class ScratchTest(ProcessorTest):
    '''Scratch blocks are unique in that they override behaviour in
    markdown and behaviour in markdown extensions, while also retaining
    compatiability.
    '''
    def __init__(self, *args, **kwargs):
        '''Sets name for loading test assets.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'scratch'

    def setUp(self):
        '''Overrides the generic setup to load the fenced_code
        extension by default (as this is the desired usecase).
        '''
        self.verto_extension = VertoExtension([self.processor_name], {}, ['markdown.extensions.fenced_code'])

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''An example of common useage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''An example showing how to override the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template}, extensions=['markdown.extensions.fenced_code'])

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Other Tests
    #~
    def test_example_standard_markdown_block(self):
        '''Tests that even without extensions it behaves as expected.
        '''
        verto_extension = VertoExtension([self.processor_name], {}, [])
        test_string = self.read_test_file(self.processor_name, 'example_standard_markdown_block.md')

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_standard_markdown_block_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_separate_blocks(self):
        '''Tests that code separated by whitespace is still processed.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_separate_blocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_separate_blocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_multiple_codeblocks(self):
        '''Tests that multiple codeblocks are processed independently.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_multiple_codeblocks_2(self):
        '''Tests that enabling the codehilite extension does not effect
        the functionality. (Loads the compatiability processor).
        '''
        extensions = ['markdown.extensions.codehilite', 'markdown.extensions.fenced_code']
        verto_extension = VertoExtension([self.processor_name], {}, extensions)
        test_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks_2.md')

        converted_test_string = markdown.markdown(test_string, extensions=extensions + [verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks_expected_2.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_other_code(self):
        '''Tests that other codeblocks that are not scratch codeblocks
        are not erroneously matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_other_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_other_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
