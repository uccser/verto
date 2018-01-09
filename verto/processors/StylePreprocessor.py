from verto.errors.StyleError import StyleError
from markdown.preprocessors import Preprocessor
import re


class StylePreprocessor(Preprocessor):
    '''
    Parses the document for custom tags and validates they meet our required style rules.
    Rules:
        All blocks tags must begin and end with a blank line.
        All block tags must be the only thing on the line.
        Disabled -- All inline tags must have a space before and after the tag.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'style'
        self.block_pattern = ext.processor_info[self.processor]['block_pattern']
        self.inline_pattern = ext.processor_info[self.processor]['inline_pattern']
        self.block_strings = ext.processor_info[self.processor]['strings']['block']
        self.inline_strings = ext.processor_info[self.processor]['strings']['inline']

        self.LIST_RE = re.compile('^[ ]*(\d+\.|[*+-])[ ]+(.*)')

    def run(self, lines):
        '''
        Validates lines and raising StyleErrors when rules are not upheld.
        Args:
            lines: A string of Markdown text.
        Returns:
            The original document.
        '''
        for i, line in enumerate(lines):
            for block_string in self.block_strings:
                c = re.compile(self.block_pattern.format(**{'block': block_string}))
                block_match = c.search(line)
                if block_match is not None:
                    # Grab important lines and their numbers
                    important_lines = (list(enumerate(lines))[max(0, i - 1): i + 2])
                    line_nums, error_lines = zip(*map(lambda x: (x[0] + 1, x[1].strip()), important_lines))

                    # Remove all empty lines, should only be one line left
                    if len([line for line in error_lines if line != '']) != 1:
                        raise StyleError(line_nums, error_lines, 'Blocks must be separated by whitespace.')

                    start_index, end_index = block_match.span()
                    rest = line[:start_index] + line[end_index+1:]

                    if (self.LIST_RE.match(line[:start_index]) and
                       not all(map(lambda char: char.isspace(), line[end_index+1:]))):
                            raise StyleError(line_nums, error_lines, 'Content after block in list.')
                    elif (not self.LIST_RE.match(line[:start_index]) and
                          not all(map(lambda char: char.isspace(), rest))):
                            raise StyleError(line_nums, error_lines, 'Blocks must be the only thing on the line.')

        return lines
