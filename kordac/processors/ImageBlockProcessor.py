from markdown.blockprocessors import BlockProcessor
import re
from kordac.processors.utils import parse_argument, centre_html
from markdown.util import etree

# NTS needs to include alt tags
class ImageBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = ext.required_files["images"]
        self.IMAGE_TEMPLATE = ext.html_templates['image']
        self.pattern = re.compile(ext.tag_patterns['image']['pattern'])

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.match(block)

        pattern_pos = match.span()
        text_before_image = block[:pattern_pos[0]]

        arguments = match.group('args')
        filename = parse_argument('filename', arguments)

        html_string = ''
        if filename:
            html_string += self.IMAGE_TEMPLATE.format(filename=filename)
            node = etree.fromstring(html_string)
            parent.append(node)

            self.required.add(filename)

