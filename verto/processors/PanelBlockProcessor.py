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

    def custom_parsing(self):
        print('custom')
        argument = 'title'
        title_r = re.compile(r'(^|\n)# ((\w| )*)(?P<args>)')
        title = title_r.search(self.content_blocks[0])
        if title:
            self.argument_values[argument] = title.groups()[1]
        else:
            raise ArgumentMissingError(self.processor, argument, '{} is a required argument.'.format(argument))

        argument = 'subtitle'
        if self.argument_values.get(argument) == 'true':
            subtitle_r = re.compile(r'(^|\n)## ((\w| )*)(?P<args>)')
            subtitle = subtitle_r.search(self.content_blocks[1])
            if subtitle:
                self.argument_values[argument] = subtitle.groups()[1]
                self.content_blocks = self.content_blocks[2:]
            else:
                raise ArgumentMissingError(self.processor, argument, '{} is set to "true" but not supplied.'.format(argument))
        elif self.argument_values.get(argument) == 'false':  # false
            del self.argument_values[argument]  # delete from argument dict so as to not be included in template
            self.content_blocks = self.content_blocks[1:]
        else:
            self.content_blocks = self.content_blocks[1:]
