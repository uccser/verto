from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument
import re
from markdown.util import etree

class ButtonLinkBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = 'button-link'
        self.BUTTON_TEMPLATE = ext.jinja_templates[self.tag]
        self.pattern = re.compile(ext.tag_patterns[self.tag]['pattern'])

    def test(self, lines):
        return self.pattern.search(lines) is not None

    def run(self, lines):
        test = ''
        for i,line in enumerate(lines):
            match = self.pattern.search(line)
            if match is not None:
                arguments = match.group('args')

                context = dict()
                context['link'] = parse_argument('link', arguments)
                context['text'] = parse_argument('text', arguments)

                lines[i] = self.BUTTON_TEMPLATE.render(context)
        return lines
