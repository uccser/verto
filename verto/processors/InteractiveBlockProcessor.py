from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
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
            argument = 'thumbnail'
            thumbnail_file_path = argument_values.get(argument, None)

            if thumbnail_file_path is not None:
                del argument_values[argument]
            else:
                thumbnail_file_path = 'interactives/{}/img/thumbnail.png'.format(name)

            external_path_match = re.search(r'^http', thumbnail_file_path)
            if external_path_match is None:  # internal image
                thumbnail_file_relative = True
                self.required_images.add(thumbnail_file_path)
            else:
                thumbnail_file_relative = False

            extra_args['thumbnail_file_path'] = thumbnail_file_path
            extra_args['thumbnail_file_relative'] = thumbnail_file_relative

        return extra_args
