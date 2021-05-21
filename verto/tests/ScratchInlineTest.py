import markdown

from verto.VertoExtension import VertoExtension
from verto.tests.ProcessorTest import ProcessorTest


class ScratchInlineTest(ProcessorTest):
    '''Scratch blocks are unique in that they override behaviour in markdown.
    '''
    def __init__(self, *args, **kwargs):
        '''Sets name for loading test assets.'''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'scratch-inline'

    def setUp(self):
        '''Overrides the generic setup to load the fenced_code
        extension by default (as this is the desired usecase).
        '''
        self.verto_extension = VertoExtension([self.processor_name], {}, ['markdown.extensions.fenced_code'])

    def test_doc_example_basic(self):
        '''An example of common useage.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''An example showing how to override the html-template.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template}, extensions=['markdown.extensions.fenced_code'])

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Other Tests
    #~

    def test_multiple_codeblocks(self):
        '''Tests that multiple codeblocks are processed independently.'''
        test_string = self.read_test_file(self.processor_name, 'multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_mixed_codeblocks(self):
        '''Tests that normal codeblocks are not inadvertently effected.'''
        extensions = ['markdown.extensions.fenced_code']
        verto_extension = VertoExtension([self.processor_name], {}, extensions)
        test_string = self.read_test_file(self.processor_name, 'mixed_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=extensions + [verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'mixed_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_codeblocks_compatibility(self):
        '''Test the codehilite and fenced_code do not causes any issues.'''
        extensions = ['markdown.extensions.codehilite', 'markdown.extensions.fenced_code']
        verto_extension = VertoExtension([self.processor_name], {}, extensions)
        test_string = self.read_test_file(self.processor_name, 'multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=extensions + [verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
