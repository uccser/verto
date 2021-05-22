import markdown
import re
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ImageInlinePattern import ImageInlinePattern
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.tests.ProcessorTest import ProcessorTest


class ImageInlineTest(ProcessorTest):
    '''Tests to check the 'image-inline' pattern works as intended.'''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for asset file retrieval.'''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'image-inline'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)
        self.ext.jinja_templates = {
            self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name),
            'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')
        }

    def test_basic_usage(self):
        '''Test common usage case.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'img/example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_doc_example_override_html(self):
        '''Basic example showing how to override the html-template.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    # ~
    # Image locations tests
    # ~

    def test_internal_image(self):
        '''Test to ensure that an internally reference image produces
        the desired output, including changing the expected images of
        the verto extension.
        '''
        test_string = self.read_test_file(self.processor_name, 'internal_image.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'internal_image_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'img/example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_external_image(self):
        '''Test that external images are processed and that the
        expected images are unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'external_image.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'external_image_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_multiple_internal_images(self):
        '''Test to ensure that an internally reference images produces
        the desired output, including changing the expected images of
        the verto extension.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_internal_images.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_internal_images_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'img/example.png',
            'img/placeholder.jpg'
        }
        self.assertSetEqual(expected_images, images)

    # ~
    # Argument tests
    # ~

    def test_missing_argument_alt(self):
        '''Test that ArgumentMissingError is thrown when alt argument is missing'''
        test_string = self.read_test_file(self.processor_name, 'missing_argument_alt.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_argument_caption(self):
        '''Test that the caption argument is correctly rendered.'''
        test_string = self.read_test_file(self.processor_name, 'argument_caption.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'argument_caption_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_argument_caption_link(self):
        '''Test that the caption-link argument is correctly rendered.'''
        test_string = self.read_test_file(self.processor_name, 'argument_caption_link.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'argument_caption_link_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_argument_source_link(self):
        '''Test that the source-link argument is correctly rendered.'''
        test_string = self.read_test_file(self.processor_name, 'argument_source_link.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'argument_source_link_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_argument_hover_text(self):
        '''Test that the hover-text argument is correctly rendered.'''
        test_string = self.read_test_file(self.processor_name, 'argument_hover_text.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'argument_hover_text_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_width_value(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        html_template = self.read_test_file(self.processor_name, 'file_width_value_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension.required_files['images']
        expected_images = {'path/to/image@500px.png'}
        self.assertSetEqual(expected_images, images)

    def test_image_width_value_no_units(self):
        '''Test image rendered correctly with width value with no units.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value_no_units.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        html_template = self.read_test_file(self.processor_name, 'file_width_value_no_units_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_no_units_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension.required_files['images']
        expected_images = {'path/to/image@900.png'}
        self.assertSetEqual(expected_images, images)

    def test_image_invalid_width_value_1(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_1.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_1_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {'path/to/image@.png'}
        self.assertSetEqual(expected_images, images)

    def test_image_invalid_width_value_2(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_2.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_2_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {'path/to/image@em20.png'}
        self.assertSetEqual(expected_images, images)

    def test_image_width_value_external_image(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value_external_image.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_external_image_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    # ~
    # Embed test.
    # ~

    def test_numbered_list(self):
        '''Test that image-inline functions within a numbered list.'''
        test_string = self.read_test_file(self.processor_name, 'numbered_list.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'numbered_list_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_table_embed(self):
        '''Test that image-inline functions within a table.'''
        test_string = self.read_test_file(self.processor_name, 'table_embed.md')

        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension, 'markdown.extensions.tables'])
        expected_string = self.read_test_file(self.processor_name, 'table_embed_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'img/example1.png',
            'img/example2.png'
        }
        self.assertSetEqual(expected_images, images)

    # ~
    # custom arguments tests.
    # ~

    def test_custom_arguments_alt_false(self):
        '''Tests to ensure that image tag is rendered correctly when alt tag is not required and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-inline': {
                    'alt': False,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'alt_false.md')
        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'alt_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'img/example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_hover_true(self):
        '''Tests to ensure that image tag is rendered correctly when hover argument is required and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-inline': {
                    'hover-text': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )


        test_string = self.read_test_file(self.processor_name, 'hover_true.md')
        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'hover_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'img/example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_alt_false_source_true(self):
        '''Tests to ensure that image tag is rendered correctly when alt argument is not required and source argument is required and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-inline': {
                    'alt': False,
                    'source': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'alt_false_source_true.md')
        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'alt_false_source_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'img/example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_hover_true_not_provided(self):
        '''Tests to ensure that correct error is raised when hover text is required and not provided.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-inline': {
                    'hover-text': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'hover_true_not_provided.md')
        processor = ImageInlinePattern(self.ext, self.md.parser)
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)
