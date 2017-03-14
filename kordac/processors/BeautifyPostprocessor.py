from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup


class BeautifyPostprocessor(Postprocessor):
    ''' Converts the output document into a more asthetically
    pleasing version with more consistent whitespace.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text):
        '''Converts the document into a more asthetically
        pleasing version.
        Args:
            text: A string of the document to convert.
        Returns:
            A string of the converted document.
        '''
        return BeautifulSoup(text, 'html.parser').prettify()
