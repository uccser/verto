from markdown.preprocessors import Preprocessor
import re


class RemoveTitlePreprocessor(Preprocessor):
    '''Removes the first found title from the given document.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the VertoExtension.
        '''
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.pattern = re.compile(ext.processor_info['title']['pattern'])

    def test(self, lines):
        '''Tests the given document to check if the processor should be
        run.

        Args:
            lines: A string of the document text.

        Result:
            True if a match is found.
        '''
        return self.pattern.search(lines) is not None

    def run(self, lines):
        '''If the title is found on the first line, remove the line.

        Args:
            lines: A list of strings that form the document.

        Returns:
            List of lines of document.
        '''
        if self.pattern.search(lines[0]) is not None:
            lines[0] = ''
        return lines
