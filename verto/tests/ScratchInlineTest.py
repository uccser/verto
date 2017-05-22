import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ScratchTreeprocessor import ScratchImageMetaData
from verto.processors.ScratchInlineTreeprocessor import ScratchInlineTreeprocessor
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

        actual_scratch_images = self.verto_extension.required_files['scratch_images']
        expected_scratch_images = {
                        ScratchImageMetaData(
                            hash='3dfa73663a21d295e1e5c1e5583d8d01edd68ec53ad3050597de126076c44ea5',
                            text='say [Hello] for (2) secs'
                        ),
                    }
        self.assertSetEqual(actual_scratch_images, expected_scratch_images)

    def test_doc_example_override_html(self):
        '''An example showing how to override the html-template.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template}, extensions=['markdown.extensions.fenced_code'])

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        actual_scratch_images = verto_extension.required_files['scratch_images']
        expected_scratch_images = {
                        ScratchImageMetaData(
                            hash='2f3ea223b778227287b8935bc5d209e25d3e8a25ef46ff85f6c44818159601d7',
                            text='when flag clicked'
                        ),
                    }
        self.assertSetEqual(actual_scratch_images, expected_scratch_images)

    #~
    # Other Tests
    #~

    def test_multiple_codeblocks(self):
        '''Tests that multiple codeblocks are processed independently.'''
        test_string = self.read_test_file(self.processor_name, 'multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        actual_scratch_images = self.verto_extension.required_files['scratch_images']
        expected_scratch_images = {
                        ScratchImageMetaData(
                            hash='3dfa73663a21d295e1e5c1e5583d8d01edd68ec53ad3050597de126076c44ea5',
                            text='say [Hello] for (2) secs'
                        ),
                        ScratchImageMetaData(
                            hash='2f3ea223b778227287b8935bc5d209e25d3e8a25ef46ff85f6c44818159601d7',
                            text='when flag clicked'
                        ),
                        ScratchImageMetaData(
                            hash='1c95862744e873cc87e4cadf6174257ce6e8a237b29b5c41f241e98e0d78eb14',
                            text='turn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual_scratch_images, expected_scratch_images)

    def test_mixed_codeblocks(self):
        '''Tests that normal codeblocks are not inadvertently effected.'''
        extensions = ['markdown.extensions.fenced_code']
        verto_extension = VertoExtension([self.processor_name], {}, extensions)
        test_string = self.read_test_file(self.processor_name, 'mixed_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=extensions + [verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'mixed_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        actual_scratch_images = verto_extension.required_files['scratch_images']
        expected_scratch_images = {
                        ScratchImageMetaData(
                            hash='9dabe0bac28bc3a143cfb19c2e5d7f46aae62b3d793166a56665a789d0df5bf7',
                            text='say [Hello]'
                        )
                    }
        self.assertSetEqual(actual_scratch_images, expected_scratch_images)


    def test_codeblocks_compatibility(self):
        '''Test the codehilite and fenced_code do not causes any issues.'''
        extensions = ['markdown.extensions.codehilite', 'markdown.extensions.fenced_code']
        verto_extension = VertoExtension([self.processor_name], {}, extensions)
        test_string = self.read_test_file(self.processor_name, 'multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=extensions + [verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        actual_scratch_images = verto_extension.required_files['scratch_images']
        expected_scratch_images = {
                        ScratchImageMetaData(
                            hash='3dfa73663a21d295e1e5c1e5583d8d01edd68ec53ad3050597de126076c44ea5',
                            text='say [Hello] for (2) secs'
                        ),
                        ScratchImageMetaData(
                            hash='2f3ea223b778227287b8935bc5d209e25d3e8a25ef46ff85f6c44818159601d7',
                            text='when flag clicked'
                        ),
                        ScratchImageMetaData(
                            hash='1c95862744e873cc87e4cadf6174257ce6e8a237b29b5c41f241e98e0d78eb14',
                            text='turn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual_scratch_images, expected_scratch_images)
