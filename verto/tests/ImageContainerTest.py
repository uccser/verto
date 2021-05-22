import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ImageContainerBlockProcessor import ImageContainerBlockProcessor
from verto.errors.ImageMissingCaptionError import ImageMissingCaptionError
from verto.errors.ImageCaptionContainsImageError import ImageCaptionContainsImageError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.tests.ProcessorTest import ProcessorTest


class ImageContainerTest(ProcessorTest):
    '''The image container processor is a simple tag with a multitude of
    different possible arguments that modify output slightly.
    Internally linked file features need to be considered
    when testing images, such that required files are modified
    and need to be checked to see if updated correctly.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name and tag argument in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'image-container'
        self.tag_argument = 'image'
        self.ext = Mock()
        self.ext.jinja_templates = {
            'image': ProcessorTest.loadJinjaTemplate(self, 'image'),
            'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')
        }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_caption_true(self):
        '''Tests to ensure that caption is rendered correctly and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'caption_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'cats.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_caption_false(self):
        '''Tests processor does not match image tag when caption argument is not included.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'caption_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_caption(self):
        '''Tests processor does not match image tag when caption argument is not included.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_alt_hover_caption(self):
        '''Tests that multiple arguments are rendered correctly when caption argument is included and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'alt_hover_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'alt_hover_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'finite-state-automata-no-trap-example.png',
            'finite-state-automata-trap-added-example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_caption_true_not_provided(self):
        '''Tests that ImageMissingCaptionError is thrown when caption argument is true but not provided.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ImageMissingCaptionError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_caption_true_missing_end_tag(self):  # throw error
        '''Tests that TagNotMatchedError is thrown when image tag is missing end tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_true_missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_caption_true_not_provided_numbered_list(self):
        '''Tests that ImageMissingCaptionError is thrown when caption argument is true but not provided in numbered list.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_true_not_provided_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ImageMissingCaptionError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_caption_true_numbered_list_missing_end_tag(self):
        '''Tests that TagNotMatchedError is thrown when image tag is missing end tag.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_true_numbered_list_missing_end_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_alt_parameter(self):
        '''Tests that missing alt argument produces correct error.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_alt_parameter.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_image_in_image_tag(self):
        '''Test that ImageCaptionContainsImageError is raised when the first line in an image container block is another image container block.
        '''
        test_string = self.read_test_file(self.processor_name, 'image_in_image_tag.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, False, True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ImageCaptionContainsImageError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_multiple_images_captions_true(self):
        '''Tests to ensure that multiple internally reference images ar rendered correctly and expected images is updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_images_captions_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, True, False, True, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_images_captions_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'the-first-image.png',
            'Lipsum.png',
            'pixel-diamond.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_multiple_images_some_captions(self):
        '''Tests to ensure that multiple internally reference images ar rendered correctly and expected images is updated and that images without captions are ignored.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_images_some_captions.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False, True, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_images_some_captions_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'finite-state-automata-no-trap-example.png',
            'finite-state-automata-trap-added-example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_external_image(self):
        '''Tests that external images are processed and that the expected images are unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'external_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'external_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_hover_text(self):
        '''Tests that argument for hover-text produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_hover_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_hover_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_caption_link(self):
        '''Tests that argument for caption-link produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_caption_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_caption_link_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_alt(self):
        '''Tests that argument for alt produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_alt.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_alt_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_source(self):
        '''Tests that argument for source produces expected output and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_source.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_source_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_left(self):
        '''Tests that argument for align produces expected output when set to left and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_left.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_left_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_right(self):
        '''Tests that argument for align produces expected output when set to right and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_right.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_right_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_center(self):
        '''Tests that argument for align produces expected output when set to center and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_center.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_center_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_undefined_error(self):
        '''Tests that ArgumentValueError is raised when undefined align value is given.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_undefined_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_image_in_numbered_list(self):
        '''Tests that image with in numbered list is rendered correctly and expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'image_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'image_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_width_value(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'file_width_value_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})
        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_width_value_no_units(self):
        '''Test image rendered correctly with width value with no units.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value_no_units.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'file_width_value_no_units_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})
        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_no_units_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_invalid_width_value_1(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_1.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'file_invalid_width_value_1_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})
        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_1_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_invalid_width_value_2(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_2.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'file_invalid_width_value_2_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})
        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_invalid_width_value_2_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_image_width_value_external_image(self):
        '''Test image rendered correctly with width value.
        '''
        test_string = self.read_test_file(self.processor_name, 'file_width_value_external_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'file_width_value_external_image_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})
        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'file_width_value_external_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_alt_false(self):
        '''Tests to ensure that image tag is rendered correctly when alt tag is not required and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-container': {
                    'alt': False,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'alt_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'alt_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'cats.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_hover_true(self):
        '''Tests to ensure that image tag is rendered correctly when hover argument is required and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-container': {
                    'hover-text': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'hover_true.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'hover_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_alt_false_source_true(self):
        '''Tests to ensure that image tag is rendered correctly when alt argument is not required and source argument is true and expected images are updated.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-container': {
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
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'alt_false_source_true_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = verto_extension_custom_rules.required_files['images']
        expected_images = {
            'cats.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_custom_arguments_hover_true_not_provided(self):
        '''Tests to ensure that correct error is raised when hover text is required and not provided.
        '''
        settings = {
            'processor_argument_overrides': {
                'image-container': {
                    'hover-text': True,
                }
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            settings=settings
        )

        test_string = self.read_test_file(self.processor_name, 'hover_true_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''Basic example of common usage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_doc_example_override_html(self):
        '''Basic example showing how to override the html-template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_doc_example_2_override_html(self):  # TODO check docstring
        '''Basic example showing how to override the html-template for relative files in a specific file only.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_2_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.tag_argument: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)
