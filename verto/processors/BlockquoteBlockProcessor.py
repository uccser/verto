from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.BlockquoteMissingFooterError import BlockquoteMissingFooterError

BLOCKQUOTE_FOOTER_PREFIX = "- "


class BlockquoteBlockProcessor(GenericContainerBlockProcessor):
    def __init__(self, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        self.processor = 'blockquote'
        super().__init__(self.processor, *args, **kwargs)

    def custom_parsing(self, content_blocks, argument_values):
        '''
        Extracts the footer of a blockquote if provided.

        Args:
            content_blocks (list): Strings to either be parsed or inserted
                                   as content in template.
            argument_values (dict): Dictionary of values to be inserted in template.

        Returns:
            Tuple containing blocks and extra_args to update the content_blocks list and argument_values dict.
        '''
        extra_args = {}
        blocks = content_blocks

        argument = 'footer'
        if argument_values.get(argument) == 'true':
            footer_index = -2
            if content_blocks[footer_index].startswith(BLOCKQUOTE_FOOTER_PREFIX):
                footer = content_blocks[footer_index]
                footer = footer[len(BLOCKQUOTE_FOOTER_PREFIX):]
                extra_args[argument] = footer
                blocks = content_blocks[:footer_index]
            else:
                raise BlockquoteMissingFooterError(self.processor, argument)
        elif argument_values.get(argument) == 'false':
            # delete from argument dict so as to not be included in template
            del argument_values[argument]

        return (blocks, extra_args)
