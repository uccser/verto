from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.errors.ArgumentValueError import ArgumentValueError
import re


class ImageTagBlockProcessor(GenericTagBlockProcessor):
    ''' Searches a Document for image tags e.g. {image file-path="<condition>"}
    adding any internal images to the verto extension final result.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
                reside in.
        '''
        self.processor = 'image-tag'
        super().__init__(self.processor, ext, *args, **kwargs)
        self.caption_pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            block: The block to be tested.

        Returns:
            True if there are any start or end tags within the block.

        Raises:
            ArgumentValueError: If value for a given argument is incorrect.
        '''
        return self.caption_pattern.search(block) is None and self.pattern.search(block) is not None

    def custom_parsing(self, argument_values):
        '''
        Extracts the caption of an image block and creates file path based on whether internal or external image.

        Args:
            content_blocks: List of strings to either be parsed or inserted as caption in template.
        Returns:
            extra_args: dictionary to update the agument_values dict.
        Raise:
        '''
        extra_args = {}

        argument = 'caption'
        # if caption is anything other than "true", image has no caption
        # TODO should raise and error if not "true" or "false" - invalid argument?
        caption_value = argument_values.get(argument)
        if  caption_value == False:
            del argument_values[argument]  # delete from dictionary so as to not be included in template
        else:
            message = 'Caption can only be "true" or "false".'
            raise ArgumentValueError(self.processor, argument, caption_value, message)

        # check if internal or external image
        file_path = argument_values['file-path']
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_path = self.relative_image_template.render({'file_path': file_path})

        extra_args['file-path'] = file_path

        return extra_args
