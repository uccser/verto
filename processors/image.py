from markdown.blockprocessors import BlockProcessor
import re
from processors.utils import parse_argument, centre_html
from markdown.util import etree

IMAGE_TEMPLATE ="""
<a href="{{% static 'main/images/{filename}' %}}" data-featherlight="image" data-featherlight-close-on-click="anywhere">
  <img src="{{% static 'main/images/{filename}' %}}" class='responsive-img'/>
</a>"""

class ImageBlockProcessor(BlockProcessor):
    p = re.compile('^\{image (?P<args>[^\}]*)\}')

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = ext.required_files.setdefault("images", [])

    def test(self, parent, block):
        return self.p.match(block) is not None

    def run(self, parent, blocks):
        match = self.p.match(blocks.pop(0))
        arguments = match.group('args')
        filename = parse_argument('filename', arguments)
        if filename:
            html = IMAGE_TEMPLATE.format(filename=filename)
            tree = etree.fromstring(html)
            parent.append(centre_html(etree.fromstring(html), 8))
            self.required.append(filename)
