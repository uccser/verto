from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.PanelMissingTitleError import PanelMissingTitleError
from verto.errors.PanelMissingSubtitleError import PanelMissingSubtitleError
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
        Raises:
            PanelMissingTitleError: If no title can be found in a panel.
            PanelMissingSubtitleError: If no subtitle can be found in a panel where it is expected.
        '''
        extra_args = {}
        blocks = []

        argument = 'title'
        title_r = re.compile(r'^#(?!#+)\s?(?P<title>.*?)$')
        title = title_r.search(content_blocks[0])
        if title:
            extra_args[argument] = title.group(argument)
        else:
            raise PanelMissingTitleError(self.processor, argument)

        argument = 'subtitle'
        if argument_values.get(argument) == 'true':
            subtitle_r = re.compile(r'^##(?!#+)\s?(?P<subtitle>.*?)$')
            subtitle = subtitle_r.search(content_blocks[1])
            if subtitle:
                extra_args[argument] = subtitle.group(argument)
                blocks = content_blocks[2:]
            else:
                raise PanelMissingSubtitleError(self.processor, argument)
        elif argument_values.get(argument) == 'false':
            del argument_values[argument]  # delete from argument dict so as to not be included in template
            blocks = content_blocks[1:]
        else:
            blocks = content_blocks[1:]

        return (blocks, extra_args)
