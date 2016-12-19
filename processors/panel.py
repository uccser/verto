from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import processors.utils as utils
import re

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
    p_start = re.compile('^\{panel ?(?P<args>[^\}]*)\}')
    p_end = re.compile('\{panel end\}')

    def test(self, parent, block):
        return re.search('\{panel ?(?P<args>[^\}]*)\}', block) is not None

    def generate_panel_tree(self, children, panel_type='', expanded=False, summary=None):

        # create a new div element
        node = etree.fromstring(PANEL_TEMPLATE)

        # pull out div and parse child elements/convert children to html
        content_node = node.find(".//div[@class='collapsible-body']")
        self.parser.parseBlocks(content_node, children)

        # change class name of list element based on type and if (not)active
        node.find(".//li[@class='panel-selector']").attrib['class'] += ' panel-{}'.format(panel_type)
        if expanded:
            node.find(".//div[@class='collapsible-body']").attrib['class'] += ' active'

        # format and place heading
        heading = utils.from_kebab_case(panel_type)
        if summary:
            heading += ': {}'.format(summary)
        heading_node = node.find(".//div[@class='panel-heading']")
        etree.SubElement(heading_node, 'strong').text = heading

        return node


    def run(self, parent, blocks):
        # block contains the match as a substring
        block = blocks.pop(0)

        # find start of match and place back in blocks list up to end of match
        m_start = self.p_start.match(block)
        blocks.insert(0, block[m_start.end():])

        # iterate over blocks until find {panel end} block
        panel_content = []
        while len(blocks) > 0:
            block = blocks.pop(0)
            m_end = self.p_end.search(block)
            if m_end is not None:
                panel_content.append(block[:m_end.start()])
                break
            else:
                # have not found end of panel, so add entire block
                panel_content.append(block)

        # create panel node and add it to parent element
        node = self.generate_panel_tree(panel_content, **get_attributes(m_start.group('args')))
        parent.append(node)


# NTS why is this function not part of the class?
def get_attributes(args):
    panel_type = utils.parse_argument('type', args)
    summary = utils.parse_argument('summary', args)
    expanded = utils.parse_argument('expanded', args)
    return {
        'panel_type': panel_type,
        'expanded': expanded,
        'summary': summary
    }

