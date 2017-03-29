from markdown.preprocessors import Preprocessor
import re


class CommentPreprocessor(Preprocessor):
    ''' Searches a Document for comments (e.g. {comment example text here})
    and removes them from the document.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Markdown parser class.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'comment'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])

    def test(self, lines):
        '''Return whether the provided document contains comments needing removal.

        Args:
            lines: A string of Markdown text.

        Returns:
            True if the document needs to be processed.
        '''
        return self.pattern.search(lines) is not None

    def run(self, lines):
        ''' Removes all instances of text that match the following
        example {comment example text here}. Inherited from
        Preprocessor class.

        Args:
            lines: A list of lines of the Markdown document to be converted.
        Returns:
            Markdown document with comments removed.
        '''
        for i, line in enumerate(lines):
            lines[i] = re.sub(self.pattern, '', line)
        return lines
