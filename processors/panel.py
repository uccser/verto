from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from processors import utils
import re
import sys

PANEL_TEMPLATE = """
<div class='clearfix'>
  <ul class='collapsible panel' data-collapsible='accordion'>
    <li class='panel-selector'>
      <div class='collapsible-header'>
        <div class='panel-heading'></div>
        <div class='dropdown-menu-arrow'>&#9660;</div>
      </div>
      <div class='collapsible-body'></div>
    </li>
  </ul>
</div>
"""

class PanelBlockProcessor(BlockProcessor):

    def test(self, parent, block):
        return re.match("^\{panel ?(?P<args>[^\}]*)\}", block) is not None

    def generate_panel_tree(self, children, panel_type='', expanded=False, summary=None):

        node = etree.fromstring(PANEL_TEMPLATE)
        content_node = node.find(".//div[@class='collapsible-body']")
        self.parser.parseBlocks(content_node, children)

        node.find(".//li[@class='panel-selector']").attrib['class'] += ' panel-{}'.format(panel_type)
        if expanded:
            node.find(".//div[@class='collapsible-body']").attrib['class'] += ' active'
        heading = utils.from_kebab_case(panel_type)
        if summary:
            heading += ': {}'.format(summary)
        heading_node = node.find(".//div[@class='panel-heading']")
        etree.SubElement(heading_node, 'strong').text = heading
        return node


    def run(self, parent, blocks):
        block = blocks.pop(0)
        m_start = re.match("^\{panel ?(?P<args>[^\}]*)\}", block)
        blocks.insert(0, block[m_start.end():])
        internal = []
        while len(blocks) > 0:
            block = blocks.pop(0)
            m_end = re.search("\{panel end\}", block)
            if m_end is not None:
                internal.append(block[:m_end.start()])
                break
            else:
                internal.append(block)

        node = self.generate_panel_tree(
            children=internal,
            **get_kwargs(m_start.group('args'))
        )
        parent.append(node)

def get_kwargs(args):
    panel_type = utils.parse_argument('type', args)
    summary = utils.parse_argument('summary', args)
    expanded = utils.parse_argument('expanded', args)
    return {
        'panel_type': panel_type,
        'expanded': expanded,
        'summary': summary
    }
