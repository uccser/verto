import markdown
from unittest.mock import Mock
from collections import defaultdict

from verto.VertoExtension import VertoExtension
from verto.processors.ImageContainerBlockProcessor import ImageContainerBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.tests.ProcessorTest import ProcessorTest

class ImageContainerTest(ProcessorTest):
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
        self.processor_name = 'image-container'
        self.ext = Mock()
        self.ext.jinja_templates = {
            'image': ProcessorTest.loadJinjaTemplate(self, 'image'),
            'relative-file-link': ProcessorTest.loadJinjaTemplate(self, 'relative-file-link')
        }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.required_files = defaultdict(set)

    def test_caption_true(self):
        '''
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
        '''
        '''
        test_string = self.read_test_file(self.processor_name, 'caption_false.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'caption_false_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_no_caption(self):
        '''
        '''
        test_string = self.read_test_file(self.processor_name, 'no_caption.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False], [ImageContainerBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_caption_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_alt_hover_caption(self):
        '''
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
