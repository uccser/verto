import markdown
from unittest.mock import Mock
from collections import defaultdict

from kordac.KordacExtension import KordacExtension
from kordac.processors.ImageBlockProcessor import ImageBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest

class ImageTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'image'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name), 'relative-image-link': ProcessorTest.loadJinjaTemplate(self, 'relative-image-link')}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_internal_image(self):
        test_string = self.read_test_file(self.processor_name, 'internal_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'internal_image_expected.html', strip=True)

        self.assertEqual(expected_string, converted_test_string)

    def test_external_image(self):
        test_string = self.read_test_file(self.processor_name, 'external_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'external_image_expected.html', strip=True)

        self.assertEqual(expected_string, converted_test_string)

    def test_default_image(self):
        test_string = self.read_test_file(self.processor_name, 'default_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'default_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_multiple_images(self):
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_images.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, True, False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_multiple_images_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_image(self):
        test_string = self.read_test_file(self.processor_name, 'no_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_text_contains_the_word_image(self):
        test_string = self.read_test_file(self.processor_name, 'text_contains_the_word_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'text_contains_the_word_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_image(self):
        test_string = self.read_test_file(self.processor_name, 'contains_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_image_and_text_contains_word_image(self):
        test_string = self.read_test_file(self.processor_name, 'contains_image_and_text_contains_word_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_image_and_text_contains_word_image_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_hover_text(self):
        test_string = self.read_test_file(self.processor_name, 'contains_hover_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_hover_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_caption_link(self):
        test_string = self.read_test_file(self.processor_name, 'contains_caption_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_caption_link_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_alt(self):
        test_string = self.read_test_file(self.processor_name, 'contains_alt.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_alt_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_caption(self):
        test_string = self.read_test_file(self.processor_name, 'contains_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_contains_source(self):
        test_string = self.read_test_file(self.processor_name, 'contains_source.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'contains_source_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_align_left(self):
        test_string = self.read_test_file(self.processor_name, 'align_left.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_left_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_align_right(self):
        test_string = self.read_test_file(self.processor_name, 'align_right.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_right_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_align_center(self):
        test_string = self.read_test_file(self.processor_name, 'align_center.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'align_center_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    # ~
    # System Tests
    # ~

    def test_internal_image_required(self):
        test_string = self.read_test_file(self.processor_name, 'internal_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

        self.assertTrue('pixel-diamond.png' in self.kordac_extension.required_files['images'])

    def test_multiple_internal_image_required(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_internal_image.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, True, True, False], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])

        self.assertTrue('pixel-diamond.png' in self.kordac_extension.required_files['images'])
        self.assertTrue('Lipsum.png' in self.kordac_extension.required_files['images'])

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_2_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [ImageBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_2_override_html_template.html', strip=True)
        link_template = self.read_test_file(self.processor_name, 'doc_example_2_override_link_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template, 'relative-image-link': link_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_2_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
