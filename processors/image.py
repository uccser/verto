from markdown.blockprocessors import BlockProcessor
import re
from processors.utils import parse_argument, centre_html
from markdown.util import etree

IMAGE_TEMPLATE ="""
<a href="{image_source}" data-featherlight="image" data-featherlight-close-on-click="anywhere">
  <img src='{image_source}' class='responsive-img'/>
</a>"""

IMAGE_ROOT = "images/"

class ImageBlockProcessor(BlockProcessor):
    p = re.compile('^\{image (?P<args>[^\}]*)\}')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filenames = set()

    def test(self, parent, block):
        return self.p.match(block) is not None

    def run(self, parent, blocks):
        match = self.p.match(blocks.pop(0))
        arguments = match.group('args')
        filename = parse_argument('filename', arguments)
        if filename:
            html = IMAGE_TEMPLATE.format(image_source=IMAGE_ROOT + filename)
            parent.append(centre_html(etree.fromstring(html), 8))
            self.filenames.add(filename)
