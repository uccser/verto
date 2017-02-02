import markdown
from markdown.preprocessors import Preprocessor
from processors.utils import parse_argument
import re
from markdown.util import etree

class ButtonPreprocessor(Preprocessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.BUTTON_TEMPLATE = ext.html_templates['button']
        self.pattern = re.compile(ext.tag_patterns['button']['pattern'])

    def test(self, lines):
        return self.pattern.search(lines) is not None

    def run(self, lines):
        new_lines = []
        for i,line in enumerate(lines):
            match = self.pattern.search(line)
            if match is not None:
                arguments = match.group('args')
                link = parse_argument('link', arguments)
                text = parse_argument('text', arguments)
                new_lines.append(self.BUTTON_TEMPLATE.format(text=text,link=link))
            elif len(line) > 0:
                new_lines.append(markdown.markdown(line))
        return new_lines

