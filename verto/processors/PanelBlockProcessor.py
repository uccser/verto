from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
import re


class PanelBlockProcessor(GenericContainerBlockProcessor):
    def __init__(self, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        self.processor = 'panel'
        super().__init__(self.processor, *args, **kwargs)

    def custom_parsing(self, content_blocks, argument_values):
        '''
        Extracts the title and subtitle of panel block's contents.

        Args:
            content_blocks: List of strings to either be parsed or inserted as content in template.
            argument_values: Dictionary of values to be inserted in template.
        Returns:
            Tuple containing blocks and extra_args to update the content_blocks list and argument_values dict.
        '''
        extra_args = {}
        blocks = []

        argument = 'title'
        title_r = re.compile(r'(^|\n)# ((\w| )*)(?P<args>)')
        title = title_r.search(content_blocks[0])
        if title:
            extra_args[argument] = title.groups()[1]
        else:
            raise ArgumentMissingError(self.processor, argument, '{} is a required argument.'.format(argument))

        argument = 'subtitle'
        if argument_values.get(argument) == 'true':
            subtitle_r = re.compile(r'(^|\n)## ((\w| )*)(?P<args>)')
            subtitle = subtitle_r.search(content_blocks[1])
            if subtitle:
                extra_args[argument] = subtitle.groups()[1]
                blocks = content_blocks[2:]
            else:
                raise ArgumentMissingError(self.processor, argument, '{} is set to "true" but not supplied.'.format(argument))  # noqa: E501
        elif argument_values.get(argument) == 'false':
            del argument_values[argument]  # delete from argument dict so as to not be included in template
            blocks = content_blocks[1:]
        else:
            blocks = content_blocks[1:]

        return (blocks, extra_args)
