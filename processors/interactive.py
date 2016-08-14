from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from processors.utils import parse_argument
from markdown.util import etree

import bs4
import re
import os

FULL_TEMPLATE = """
{{% extends "main/index.html" %}}

{{% block content %}}
{content}
{{% endblock %}}

{{% block page-scripts %}}
{scripts}
{{% endblock %}}
"""

class InteractivePostProcessor(Postprocessor):
    def __init__(self, iBlockProcessor, *args, **kwargs):
        self.ibp = iBlockProcessor
        super().__init__(*args, **kwargs)

    def run(self, text):
        return FULL_TEMPLATE.format(
            content = text,
            scripts = '\n'.join(self.ibp.scripts)
        )

class InteractiveBlockProcessor(BlockProcessor):
    p = re.compile('^\{interactive ?(?P<args>[^\}]*)\}$')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.inpage = set()
        self.scripts = []

    def test(self, parent, block):
        return self.p.match(block) is not None

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        match = self.p.match(blocks.pop(0))
        arguments = match.group('args')
        name = parse_argument('name', arguments)
        interactive_type = parse_argument('type', arguments)
        if name and interactive_type == 'in-page':
            dj_tag ='\n{{% include \'interactive/{}/interactive.html\' %}}\n'.format(name)
            if sibling is not None:
                sibling.tail = sibling.tail or '' +  dj_tag
            else:
                parent.text = parent.text or '' + dj_tag
            self.scripts.append('\n{{% include \'interactive/{}/scripts.html\' %}}\n'.format(name))
