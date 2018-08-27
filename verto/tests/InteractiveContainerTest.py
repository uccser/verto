import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.InteractiveContainerBlockProcessor import InteractiveContainerBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.InteractiveTextContainsInteractiveError import InteractiveTextContainsInteractiveError
from verto.errors.InteractiveMissingTextError import InteractiveMissingTextError
from verto.tests.ProcessorTest import ProcessorTest


class InteractiveContainerTest(ProcessorTest):
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
        self.processor_name = 'interactive-container'
        self.tag_argument = 'interactive'
        self.ext = Mock()
        self.ext.jinja_templates = {'interactive': ProcessorTest.loadJinjaTemplate(self, 'interactive')}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_whole_page_external_thumbnail(self):
        '''Test external image for image thumbnail.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_external_thumbnail.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

    def test_text_true_not_provided(self):
        '''Tests that InteractiveMissingTextError is thrown when text argument is true but not provided.
        '''
        test_string = self.read_test_file(self.processor_name, 'text_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(InteractiveMissingTextError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_text_true_missing_end_tag(self):
        '''Tests that TagNotMatchedError is thrown when interactive tag is missing end tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'text_true_missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_multiple_interactives_text_true(self):
        '''Test multiple interactives in one file are all correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_interactives_text_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False, True, False, True, False, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_interactives_text_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards',
                'arrows',
                'flying-boxes'
            },
            'images': {
                'binarycards.png',
                'interactives/arrows/img/thumbnail.png',
                'interactives/flying-boxes/img/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }

        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_contains_multiple_interactives_some_text(self):
        '''Test multiple interactives in one file are all correctly parsed, and ignores those without text.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_interactives_some_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, False, False, False, False, False, False, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_interactives_some_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'binary-cards',
            },
            'images': {
                'binarycards.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_text_false(self):
        '''Tests processor does not match interactive tag when text argument is false.
        '''
        test_string = self.read_test_file(self.processor_name, 'text_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'text_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': set(),
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_no_text(self):
        '''Tests processor does not match interactive tag when text argument is not included.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': set(),
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_interactive_in_interactive_tag(self):
        '''Test that InteractiveTextContainsInteractiveError is raised when the first line in an interactive container block is another interactive container block.
        '''
        test_string = self.read_test_file(self.processor_name, 'interactive_in_interactive_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(InteractiveTextContainsInteractiveError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_whole_page_parameters(self):
        '''Test whole page interactive with parameters is correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'whole_page_parameters.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

        self.assertListEqual([True, False, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

    def test_iframe(self):
        '''Test iframe interactive is ignored.
        '''
        test_string = self.read_test_file(self.processor_name, 'iframe.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'iframe_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': set(),
            'images': set(),
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_missing_type(self):
        '''Test ArgumentMissingError is raised when interactive type is not given.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_invalid_type(self):
        '''Test ArgumentValueError is raised when interactive type is not valid.
        '''
        test_string = self.read_test_file(self.processor_name, 'invalid_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_multiple_interactives(self):
        '''Test multiple interactives in one file are all correctly parsed.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_interactives.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_interactives_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        required_files = {
            'interactives': {
                'arrows',
                'flying-boxes'
            },
            'images': {
                'interactives/arrows/img/thumbnail.png',
                'interactives/flying-boxes/img/thumbnail.png'
            },
            'page_scripts': set(),
            'scratch_images': set()
        }
        self.assertEqual(self.verto_extension.required_files, required_files)

    def test_custom_arguments_parameters_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when parameters argument is not required.
        '''
        custom_argument_rules = {
            "interactive-container": {
                "parameters": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'parameters_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'parameters_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when thumbnail argument is not required.
        '''
        custom_argument_rules = {
            "interactive-container": {
                "thumbnail": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'thumbnail_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_text_true_not_provided(self):
        '''Tests to ensure that correct error is raised when text is required and not provided.
        '''
        custom_argument_rules = {
            "interactive-container": {
                "text": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'text_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, True, False], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(InteractiveMissingTextError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    def test_custom_arguments_parameters_and_thumbnail_true(self):
        '''Tests to ensure that interactive tag is rendered correctly when text and thumbnail arguments are required.
        '''
        custom_argument_rules = {
            "interactive-container": {
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

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'parameters_and_thumbnail_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_whole_page(self):
        '''Example of a whole-page interactive.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_whole_page_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

    def test_doc_example_override_html(self):
        '''Example showing overriding the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [InteractiveContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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
