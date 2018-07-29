import markdown
from unittest.mock import Mock
from collections import defaultdict, OrderedDict
import json
import pkg_resources

from verto.VertoExtension import VertoExtension
from verto.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
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
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.required_files = defaultdict(set)

    def test_whole_page_external_thumbnail(self):
        '''Test external image for image thumbnail.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_external_thumbnail.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_external_thumbnail_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_text(self):
        '''Test whole page interactive with text is correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': {
                'interactives/binary-cards/img/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_parameters(self):
        '''Test whole page interactive with parameters is correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': {
                'interactives/binary-cards/img/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_thumbnail(self):
        '''Test whole page interactive with thumbnail is correctly parsed and thumbnail path is added to required files.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': {
                'interactives/binary-cards/img/binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_whole_page_thumbnail_parameters(self):
        '''Test whole page interactive with thumbnail and parameters is correctly parsed and thumbnail path is added to required files.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_thumbnail_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_iframe_parameters(self):
        '''Test iframe interactive with parameters is correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'iframe_parameters_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                "binary-cards"
            },
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_in_page_missing_name(self):
        '''Test ArgumentMissingError is raised when interactive name is not given.
        '''
        test_string = self.read_test_file(self.processor_name, 'in_page_missing_name.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_type(self):
        '''Test ArgumentMissingError is raised when interactive type is not given.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_invalid_type(self):
        '''Test ArgumentValueError is raised when interactive type is not valid.
        '''
        test_string = self.read_test_file(self.processor_name, 'invalid_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_multiple_interactives(self):
        '''Test multiple interactives in one file are all correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_interactives.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_interactives_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards',
                'arrows',
                'flying-boxes'
            },
            'images': {
                'binarycards.png'
            },
            'page_scripts': {
                'interactive/flying-boxes/scripts.html'
            },
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_custom_arguments_text_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when text argument is not required.
        '''
        json_data = pkg_resources.resource_string('verto', 'tests/assets/interactive/text_true_custom_argument_rules.json').decode('utf-8')
        custom_argument_rules = json.loads(json_data, object_pairs_hook=OrderedDict)
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'text_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'text_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_parameters_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when parameters argument is not required.
        '''
        json_data = pkg_resources.resource_string('verto', 'tests/assets/interactive/parameters_true_custom_argument_rules.json').decode('utf-8')
        custom_argument_rules = json.loads(json_data, object_pairs_hook=OrderedDict)
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'parameters_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'parameters_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when thumbnail argument is not required.
        '''
        json_data = pkg_resources.resource_string('verto', 'tests/assets/interactive/thumbnail_true_custom_argument_rules.json').decode('utf-8')
        custom_argument_rules = json.loads(json_data, object_pairs_hook=OrderedDict)
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'thumbnail_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_text_true_not_provided(self):
        '''Tests to ensure that correct error is raised when text is required and not provided.
        '''
        json_data = pkg_resources.resource_string('verto', 'tests/assets/interactive/text_true_custom_argument_rules.json').decode('utf-8')
        custom_argument_rules = json.loads(json_data, object_pairs_hook=OrderedDict)
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'text_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    def test_custom_arguments_text_and_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when text and thumbnail arguments are required.
        '''
        json_data = pkg_resources.resource_string('verto', 'tests/assets/interactive/text_and_thumbnail_true_custom_argument_rules.json').decode('utf-8')
        custom_argument_rules = json.loads(json_data, object_pairs_hook=OrderedDict)
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'text_and_thumbnail_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'text_and_thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    # ~
    # Doc Tests
    # ~

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
            'interactives': {
                "binary-cards"
            },
            'images': {
                'interactives/binary-cards/img/thumbnail.png'
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
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards'
            },
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(verto_extension.required_files, required_files)
