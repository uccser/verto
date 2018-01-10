from markdown.preprocessors import Preprocessor
import re


class SaveTitlePreprocessor(Preprocessor):
    ''' Saves the first title found in the document to
    the VertoExtension as part of the final result.
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
        ''' Tests the given document to check if the processor should be
        run.

        Args:
            lines: A string of the document text.

        Result:
            True if a match is found.
        '''
        return self.pattern.search(lines) is not None

    def run(self, lines):
        '''Saves title on first line to the VertoExtension.

        Args:
            lines: A list of strings that form the document.

        Returns:
            The original list of strings of document.
        '''
        match = self.pattern.search(lines[0])
        if match is not None:
            self.ext.title = match.group(1)
        return lines
