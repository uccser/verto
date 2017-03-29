from markdown.postprocessors import Postprocessor
from html import unescape
import re

class JinjaPostprocessor(Postprocessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text):
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
