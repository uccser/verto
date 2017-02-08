from markdown.blockprocessors import BlockProcessor
import re
from kordac.processors.utils import parse_argument, centre_html
from markdown.util import etree
import jinja2

# NTS needs to include alt tags
class ImageBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = ext.required_files["images"]
        # self.IMAGE_TEMPLATE = ext.html_templates['image']
        self.pattern = re.compile(ext.tag_patterns['image']['pattern'])
        self.template = ext.jinja_templates['image']

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.match(block)

        pattern_pos = match.span()
        text_before_image = block[:pattern_pos[0]]

        arguments = match.group('args')

        context = dict()
        context['file_path'] = parse_argument('file_path', arguments)
        context['alt'] = parse_argument('alt', arguments)
        context['title'] =  parse_argument('title', arguments)
        context['caption'] = parse_argument('caption', arguments)
        context['caption_link'] = parse_argument('caption_link', arguments)
        context['source_link'] = parse_argument('source_link', arguments)
        context['alignment'] = parse_argument('alignment', arguments)
        context['hover_text'] =  parse_argument('hover_text', arguments)

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)

        self.required.add(context['file_path'])

