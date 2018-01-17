from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.ImageMissingCaptionError import ImageMissingCaptionError
from verto.errors.ImageCaptionContainsImageError import ImageCaptionContainsImageError
from verto.utils.image_file_name_components import image_file_name_components
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
        self.processor = 'image-container'
        super().__init__(self.processor, ext, *args, **kwargs)
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.required = ext.required_files['images']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            block: The block to be tested.

        Returns:
            True if there are any start or end tags within the block.
        '''
        return self.pattern.search(block) is not None or self.p_end.search(block) is not None

    def custom_parsing(self, content_blocks, argument_values):
        '''
        Extracts the caption of an image block and creates file path based on whether internal or external image.

        Args:
            content_blocks (list): List of strings to either be parsed or inserted as caption in template.
            argument_values (dict): Dictionary of arguments and values provided in tag block.
        Returns:
            Tuple containing blocks (list) and extra_args (dict) to update the content_blocks list and
                agument_values dict.
        Raises:
            ImageCaptionContainsImageError: If the first line of an image block is another image block.
            ImageMissingCaptionError: If no caption can be found in the image block.
        '''
        for block in content_blocks:
            if self.p_start.search(block):
                raise ImageCaptionContainsImageError(self.processor)

        extra_args = {}

        argument = 'caption'
        if len(content_blocks) == 0 or content_blocks[0] == '':
            raise ImageMissingCaptionError(self.processor, argument)
        extra_args[argument] = content_blocks[0]

        file_path = argument_values['file-path']
        del(argument_values['file-path'])
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_relative = True
            extra_args.update(image_file_name_components(file_path))
        else:
            file_relative = False
        extra_args['full_file_path'] = file_path
        extra_args['file_relative'] = file_relative

        return (content_blocks, extra_args)
