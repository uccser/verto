from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
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
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

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
        if argument_values.get('caption'):
            del argument_values[argument]  # delete from dictionary so as to not be included in template

        # check if internal or external image
        file_path = argument_values['file-path']
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_path = self.relative_image_template.render({'file_path': file_path})

        extra_args['file-path'] = file_path

        return extra_args
