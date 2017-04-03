import markdown
from unittest.mock import Mock
from verto.VertoExtension import VertoExtension
from verto.processors.RemoveTitlePreprocessor import RemoveTitlePreprocessor
from verto.tests.ProcessorTest import ProcessorTest

class RemoveTitleTest(ProcessorTest):
    '''Tests to check the 'remove-title' preprocesser works as intended.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for asset file retrieval.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'remove-title'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_basic_usage(self):
        '''Tests that common usecase works as expected.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_headings(self):
        '''Tests that multiple matches of the common usecase are
        found and processed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_level_one_headings(self):
        '''Tests that only the first of the level one headings is
        removed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_level_one_headings_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

    def test_no_headings(self):
        '''Tests that the text of a document with no heading is
        unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_headings.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_headings_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_level_two_heading(self):
        '''Tests that a level two heading is also removed if found
        first.
        '''
        test_string = self.read_test_file(self.processor_name, 'level_two_heading.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'level_two_heading_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_heading_permalink(self):
        '''Tests that generic text with a permalink is uneffected.
        (So that there is no assumption of removing the first
        permalink)
        '''
        test_string = self.read_test_file(self.processor_name, 'no_heading_permalink.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertFalse(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_heading_permalink_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_space_title(self):
        '''Tests that the all the heading is removed if spaces
        are present.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_space_title.md')

        processor = RemoveTitlePreprocessor(self.ext, self.md.parser)
        self.assertTrue(processor.test(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_space_title_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)


    # SYSTEM TESTS

    def test_processor_off(self):
        '''Tests that disabling the processor, leaves the document
        unchanged.
        '''
        # Create Verto extension without processor enabled (off by default)
        verto_extension = VertoExtension()
        test_string = self.read_test_file(self.processor_name, 'processor_off.md')

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'processor_off_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
