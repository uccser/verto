from markdown.postprocessors import Postprocessor
from html import unescape
import re


class JinjaPostprocessor(Postprocessor):
    ''' Checks all jinja blocks in the output and ensures that they
    are not escaped like other html blocks.
    '''

    def __init__(self, *args, **kwargs):
        ''' Creates a new JinjaPostprocessor.
        '''
        super().__init__(*args, **kwargs)

    def run(self, text):
        '''
        Args:
            text: A string of the document.
        Returns:
            The document text with all Jinja blocks unescaped.
        '''
        r = re.compile(r'{% ([^}])*}(?<= %})')

        out = ''
        match = r.search(text)
        while match is not None:
            string = match.group()
            string = unescape(string)

            out += text[:match.start()] + string
            text = text[match.end():]
            match = r.search(text)
        out += text
        return out
