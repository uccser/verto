from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument
import re
from markdown.util import etree

class ButtonLinkBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'button-link'
        self.template = ext.jinja_templates[self.processor]
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.search(block)

        arguments = match.group('args')
        context = dict()
        context['link'] = parse_argument('link', arguments)
        context['text'] = parse_argument('text', arguments)

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
