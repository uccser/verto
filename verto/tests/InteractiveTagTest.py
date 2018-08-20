import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.InteractiveTagBlockProcessor import InteractiveTagBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.tests.ProcessorTest import ProcessorTest


class InteractiveTagTest(ProcessorTest):
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
        self.processor_name = 'interactive-tag'
        self.tag_argument = 'interactive'
        self.ext = Mock()
        self.ext.jinja_templates = {'interactive': ProcessorTest.loadJinjaTemplate(self, 'interactive')}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_whole_page_text(self):
        '''Test whole page interactive with text is ignored.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'whole_page_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': set(),
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_iframe_parameters(self):
        '''Test iframe interactive with parameters is correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_type(self):
        '''Test ArgumentMissingError is raised when interactive type is not given.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_invalid_type(self):
        '''Test ArgumentValueError is raised when interactive type is not valid.
        '''
        test_string = self.read_test_file(self.processor_name, 'invalid_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_multiple_interactives(self):
        '''Test multiple interactives in one file are all correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_interactives.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

    def test_custom_arguments_parameters_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when parameters argument is required.
        '''
        custom_argument_rules = {
            "interactive-tag": {
                "parameters": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'parameters_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'parameters_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when thumbnail argument is required.
        '''
        custom_argument_rules = {
            "interactive-tag": {
                "thumbnail": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'thumbnail_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_parameters_and_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when type argument is not required and parameters argument is required.
        '''
        custom_argument_rules = {
            "interactive-tag": {
                "parameters": True,
                "thumbnail": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'parameters_and_thumbnail_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'parameters_and_thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_in_page(self):
        '''Example of an in-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_in_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

    def test_doc_example_iframe(self):
        '''Example of an iframe interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_iframe_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

        self.assertListEqual([True], [InteractiveTagBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})

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
