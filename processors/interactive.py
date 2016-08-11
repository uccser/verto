from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from processors.utils import parse_argument
from markdown.util import etree

# import lxml.etree
import bs4
# import lxml.html.soupparser
import re
import os

INTERACTIVES_ROOT = 'interactives'

class InteractiveBlockProcessor(BlockProcessor):
    p = re.compile('^\{interactive ?(?P<args>[^\}]*)\}')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inpage = set()
        self.scripts = set()

    def test(self, parent, block):
        return self.p.match(block) is not None

    def run(self, parent, blocks):
        match = self.p.match(blocks.pop(0))
        arguments = match.group('args')
        name = parse_argument('name', arguments)
        interactive_type = parse_argument('type', arguments)
        if name and interactive_type == 'in-page':
            with open(os.path.join('output', INTERACTIVES_ROOT, name, 'index.html')) as f:
                html = f.read()
            bs = bs4.BeautifulSoup(html, "html5lib")
            bs = bs.find('div', {'id': 'interactive-{}'.format(name)})
            self.modify(bs, name)
            parent.append(etree.fromstring(bs.prettify()))


    def modify(self, root, iname):
        link_attributes = ['href', 'src']
        for element in root.find_all():
            for attr in link_attributes:
                raw_link = element.get(attr, None)
                if raw_link and not raw_link.startswith('http://') and not raw_link == '#':
                    link = os.path.join(INTERACTIVES_ROOT, iname, raw_link)
                    element[attr] = link
            if element.name == 'script' or (element.name == 'link' and element.get('rel', None) == ['stylesheet']):
                self.scripts.add(element.extract().prettify())


class InteractiveTreeProcessor(Treeprocessor):
    def __init__(self, blockProcessor, *args, **kwargs):
        self.blockProcessor = blockProcessor
        super().__init__(*args, **kwargs)

    def run(self, root):
        print('yay!')
        print(self.blockProcessor.scripts)
        body = root.find(".//body")
        for script in self.blockProcessor.scripts:
            root.append(etree.fromstring(script))
