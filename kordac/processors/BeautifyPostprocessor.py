from markdown.postprocessors import Postprocessor
from bs4 import BeautifulSoup

class BeautifyPostprocessor(Postprocessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text):
        return BeautifulSoup(text, 'html.parser').prettify()
