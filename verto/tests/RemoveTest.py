import markdown
from verto.VertoExtension import VertoExtension
from verto.tests.ProcessorTest import ProcessorTest

class RemoveTest(ProcessorTest):
    '''Removes tags <remove> and </remove> from the document.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'remove'

    def test_doc_example_basic(self):
        '''Checks that basic usecase works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
