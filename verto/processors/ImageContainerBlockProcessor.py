from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.processors.utils import parse_arguments
from verto.utils.HtmlParser import HtmlParser
import re


class ImageContainerBlockProcessor(GenericContainerBlockProcessor):
    ''' Searches a Document for image tags e.g. {image file-path="<condition>"}
    adding any internal images to the verto extension final result.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
                reside in.
        '''
        self.processor = 'image_container'
        super().__init__(self.processor, ext, *args, **kwargs)
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            block: The block to be tested.
        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.search(block) is not None

    def custom_parsing(self, content_blocks, argument_values):
        print('image container custom parsing')
        return (content_blocks, {})
