import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from verto.tests.ProcessorTest import ProcessorTest


class InteractiveTest(ProcessorTest):
    '''The interactive processor is a simple tag with a complex
    output that relies on external systems.
    When writing tests whether or not the thumbnail is externally
    or internally linked will changed output. If the thumbnail is
    internal then the required files must be modified to include
    this image.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'interactive'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name), 'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')}
        self.ext.required_files = defaultdict(set)

    def test_whole_page_text(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binary-cards/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_parameters(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binary-cards/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_thumbnail(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_thumbnail_parameters(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_iframe_parameters(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'iframe_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binary-cards/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_iframe_thumbnail(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe_thumbnail.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'iframe_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binary-cards/binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_iframe_thumbnail_parameters(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe_thumbnail_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'iframe_thumbnails_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_in_page_missing_name(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'in_page_missing_name.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

    def test_missing_type(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_type.md')
        blocks = self.to_blocks(test_string)

    def test_invalid_type(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'invalid_type.md')
        blocks = self.to_blocks(test_string)

    def test_doc_example_in_page(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_in_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_in_page_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards'
            },
            'images': set(),
            'page_scripts': {
                'interactive/binary-cards/scripts.html'
            },
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_multiple_interactives(self):
        pass

    def test_doc_example_whole_page(self):
        '''Example of a whole-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_whole_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_whole_page_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {"binary-cards"},
            'images': {
                'binary-cards/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_doc_example_iframe(self):
        '''Example of an iframe interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_iframe_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_iframe_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards'
            },
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_doc_example_override_html(self):
        '''Example showing overriding the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
