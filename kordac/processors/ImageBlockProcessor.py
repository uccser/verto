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

        file_path = parse_argument('file_path', arguments)
        alt = parse_argument('alt', arguments)
        title = parse_argument('title', arguments)
        caption = parse_argument('caption', arguments)
        caption_link = parse_argument('caption_link', arguments)
        source = parse_argument('source', arguments)
        alignment = parse_argument('alignment', arguments)
        hover_text = parse_argument('hover_text', arguments)

        context = dict()
        context['file_path'] = file_path
        context['alt'] = alt
        context['title'] = title
        context['caption'] = caption
        context['caption_link'] = caption_link
        context['source'] = source
        context['alignment'] = alignment
        context['hover_text'] = hover_text

        print(context)


        html_string = self.template.render(context)
        print(html_string)
        print()
        # html_string += self.IMAGE_TEMPLATE.format(filename=filename)
        node = etree.fromstring(html_string)
        parent.append(node)

        self.required.add(file_path)

