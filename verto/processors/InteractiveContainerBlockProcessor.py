from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.InteractiveTextContainsInteractiveError import InteractiveTextContainsInteractiveError
from verto.errors.InteractiveMissingTextError import InteractiveMissingTextError

import re


class InteractiveContainerBlockProcessor(GenericContainerBlockProcessor):
    ''' Searches a Document for interactive tags e.g.
        {interactive slug='example' type='in-page'}.
        These are then replaced with the html template.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
                reside in.
        '''
        self.processor = 'interactive-container'
        super().__init__(self.processor, ext, *args, **kwargs)
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])

        self.scripts = ext.required_files['page_scripts']
        self.required_interactives = ext.required_files['interactives']
        self.required_images = ext.required_files['images']

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
        Extracts the text of an interactive block.

        Args:
            content_blocks (list): List of strings to either be parsed or inserted as caption in template.
            argument_values (dict): Dictionary of arguments and values provided in tag block.
        Returns:
            Tuple containing blocks (list) and extra_args (dict) to update the content_blocks list and
                agument_values dict.
        Raises:

        '''
        for block in content_blocks:
            if self.p_start.search(block):
                raise InteractiveTextContainsInteractiveError(self.processor)

        extra_args = {}

        argument = 'text'
        if len(content_blocks) == 0 or content_blocks[0] == '':
            raise InteractiveMissingTextError(self.processor, argument)
        extra_args[argument] = content_blocks[0]

        interactive_type = argument_values['type']
        slug = argument_values['slug']

        # add to list of interactives
        self.required_interactives.add(slug)

        if interactive_type == 'whole-page':
            argument = 'thumbnail'
            thumbnail_file_path = argument_values.get(argument, None)

            if thumbnail_file_path is not None:
                del argument_values[argument]
            else:
                thumbnail_file_path = 'interactives/{}/img/thumbnail.png'.format(slug)

            external_path_match = re.search(r'^http', thumbnail_file_path)
            if external_path_match is None:  # internal image
                thumbnail_file_relative = True
                self.required_images.add(thumbnail_file_path)
            else:
                thumbnail_file_relative = False

            extra_args['thumbnail_file_path'] = thumbnail_file_path
            extra_args['thumbnail_file_relative'] = thumbnail_file_relative

        return (content_blocks, extra_args)
