from markdown.blockprocessors import BlockProcessor
from processors.utils import parse_argument, centre_html
from markdown.util import etree
import re

IMAGE_TEMPLATE ="""
<a href="{{% static 'main/images/{filename}' %}}" data-featherlight="image" data-featherlight-close-on-click="anywhere">
  <img src="{{% static 'main/images/{filename}' %}}" class='responsive-img'/>
</a>"""

class ImageBlockProcessor(BlockProcessor):
    pattern = re.compile('^\{image (?P<args>[^\}]*)\}')

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = ext.required_files["images"]

    def test(self, parent, block):
        return self.pattern.match(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.match(block)

        # pull out file name for image
        arguments = match.group('args')
        filename = parse_argument('filename', arguments)
        if filename:
            html = IMAGE_TEMPLATE.format(filename=filename)
            tree = etree.fromstring(html)
            parent.append(centre_html(etree.fromstring(html), 8))
            # add file name to list of required files
            self.required.add(filename)
