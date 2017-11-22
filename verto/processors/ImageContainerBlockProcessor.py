from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
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
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])  # TODO update regex to only find caption, ignore other args
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

    def test(self, parent, block):
        '''
        '''
        return self.pattern.search(block) is not None or self.p_end.search(block) is not None

    def custom_parsing(self, content_blocks, argument_values):
        '''
        '''
        extra_args = {}
        extra_args['caption'] = content_blocks[0]

        file_path = argument_values['file-path']
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_path = self.relative_image_template.render({'file_path': file_path})

        extra_args['file-path'] = file_path

        return (content_blocks, extra_args)
