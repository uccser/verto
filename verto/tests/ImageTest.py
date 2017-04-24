import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ImageBlockProcessor import ImageBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.tests.ProcessorTest import ProcessorTest

class ImageTest(ProcessorTest):
    '''The image processor is a simple tag with a multitude of
    different possible arguments that modify output slightly.
    Internally linked file features need to be considered
    when testing images, such that required files are modified
    and need to be checked to see if updated correctly.
    '''

    def __init__(self, *args, **kwargs):
        '''Set processor name in class for file names.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'image'
        self.ext = Mock()
        self.ext.jinja_templates = {
            self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name),
            'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')
        }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_internal_image(self):
        '''Tests to ensure that an internally reference image
        produces the desired output, including changing the
        expected images of the verto extension.
        '''
        test_string = self.read_test_file(self.processor_name, 'internal_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'internal_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'pixel-diamond.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_external_image(self):
        '''Tests that external images are processed and that
        the expected images are unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'external_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'external_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_default_image(self):
        '''Tests that old image tags retain compatability.
        '''
        test_string = self.read_test_file(self.processor_name, 'default_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'default_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_multiple_images(self):
        '''Tests that multiple internal images are processed correctly
        and that the expected images are updated.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_images.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_images_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'finite-state-automata-no-trap-example.png',
            'finite-state-automata-trap-added-example.png',
            'finite-state-automata-trap-added-extreme-example.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_text_contains_the_word_image(self):
        '''Tests that text containing the processor name is
        not matched erroneously.
        '''
        test_string = self.read_test_file(self.processor_name, 'text_contains_the_word_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'text_contains_the_word_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_contains_image_and_text_contains_word_image(self):
        '''Tests that text containing the processor name does
        not affect processing of actual image tags.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_image_and_text_contains_word_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_image_and_text_contains_word_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'pixel-diamond.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_hover_text(self):
        '''Tests that argument for hover-text produces expected output.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_hover_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_hover_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_caption_link(self):
        '''Tests that argument for caption-link produces expected output.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_caption_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_caption_link_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_alt(self):
        '''Tests that argument for alt produces expected output.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_alt.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_alt_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_caption(self):
        '''Tests that argument for caption produces expected output.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_contains_source(self):
        '''Tests that argument for source produces expected output.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_source.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_source_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_left(self):
        '''Tests that argument for align produces expected output
        when set to left.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_left.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_left_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_right(self):
        '''Tests that argument for align produces expected output
        when set to right.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_right.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_right_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_align_center(self):
        '''Tests that argument for align produces expected output
        when set to center.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_center.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_center_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = {
            'computer-studying-turing-test.png'
        }
        self.assertSetEqual(expected_images, images)

    def test_caption_link_error(self):
        '''Tests that the argument for caption-link throughs the
        ArgumentMissingError when caption is not provided.
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_link_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_align_undefined_error(self):
        '''Tests that undefined align value produces
        the ArgumentValueError.
        '''
        test_string = self.read_test_file(self.processor_name, 'align_undefined_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentValueError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_image_in_numbered_list(self):
        '''Basic example of common usage.'''
        test_string = self.read_test_file(self.processor_name, 'image_in_numbered_list.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'image_in_numbered_list_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''Basic example of common usage.'''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)

    def test_doc_example_2_override_html(self):
        '''Basic example showing how to override the html-template
        for relative files in a specific file only.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_2_override_html_template.html', strip=True)
        link_template = self.read_test_file(self.processor_name, 'doc_example_2_override_link_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template, 'relative-file-link': link_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        images = self.verto_extension.required_files['images']
        expected_images = set()
        self.assertSetEqual(expected_images, images)
