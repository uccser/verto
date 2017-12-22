from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.processors.utils import parse_arguments
from verto.utils.HtmlParser import HtmlParser
import re


class InteractiveBlockProcessor(GenericTagBlockProcessor):
    '''Searches a Document for interactive tags:
        e.g. {interactive name='example' type='in-page'}
        These are then replaced with the html template.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        self.processor = 'interactive'
        super().__init__(self.processor, ext, *args, **kwargs)
        self.interactive_thumbnail_path_template = ext.jinja_templates['interactive-thumbnail-path']
        self.scripts = ext.required_files['page_scripts']
        self.required_interactives = ext.required_files['interactives']
        self.required_images = ext.required_files['images']

    def custom_parsing(self, argument_values):
        '''Determines the file path to use for an interactive's thumbnail.

        Args:
            argument_values (dict): Dictionary of arguments and values provided in tag block.
        Returns:
            extra_args (dict): dictionary to update the agument_values dict.
        '''
        extra_args = {}
        interactive_type = argument_values['type']
        name = argument_values['name']

        # add to list of interactives
        self.required_interactives.add(name)

        if interactive_type == 'in-page':
            self.scripts.add('interactive/{}/scripts.html'.format(name))
        elif interactive_type == 'whole-page':
            thumbnail_path = argument_values.get('thumbnail', 'thumbnail.png')
            external_path_match = re.search(r'^http', thumbnail_path)
            if external_path_match is None:  # internal image
                self.required_images.add(thumbnail_path)
                file_path = self.interactive_thumbnail_path_template.render({'file_path': thumbnail_path, 'name': name})
            extra_args['file-path'] = file_path

        return extra_args
