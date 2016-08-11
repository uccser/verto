from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from processors import utils
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

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        if sibling is not None and sibling.tag == 'panel':
            return True
        return re.match("^\{panel ?(?P<args>[^\}]*)\}", block) is not None

    def generate_panel_tree(self, panel_node):
        attrib = panel_node.attrib
        node = etree.fromstring(PANEL_TEMPLATE)
        content_node = node.find(".//div[@class='collapsible-body']")
        for child in panel_node:
            content_node.append(child)
        print([n for n in content_node])
        node.find(".//li[@class='panel-selector']").attrib['class'] += ' panel-{}'.format(attrib['type'])
        if attrib.get('expanded'):
            node.find(".//div[@class='collapsible-body']").attrib['class'] += ' active'
        heading = utils.from_kebab_case(attrib.get('type'))
        if attrib.get('summary'):
            heading += ': {}'.format(attrib.get('summary'))
        heading_node = node.find(".//div[@class='panel-heading']")
        etree.SubElement(heading_node, 'strong').text = heading
        return node

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        if sibling.tag == "panel":
            panel = sibling
            m = re.match("\{panel end\}", block)
            if m:
                self.parser.parseBlocks(panel, panel.attrib.pop('blocks'))
                parent[-1] = self.generate_panel_tree(panel)
            else:
                panel.attrib.setdefault("blocks", []).append(block)
        else:
            m = re.match("^\{panel ?(?P<args>[^\}]*)\}", block)
            print('creating tag')
            panel = etree.SubElement(parent, 'panel')
            self.set_attribs(panel, m.group('args'))


    def set_attribs(self, panel_element, args):
        panel_type = utils.parse_argument('type', args)
        summary = utils.parse_argument('summary', args)
        expanded = utils.parse_argument('expanded', args)
        panel_element.attrib.update({
            'type': panel_type,
            'expanded': expanded,
            'summary': summary
        })




class PanelPreprocessor(Preprocessor):
    """Ensure all panel tags are surrounded by at least one empty line, and so
    are their own block
    """
    def run(self, lines):
        p = re.compile(r'^\{panel ?(?P<args>[^\}]*)\}')
        i = 0
        while i < len(lines):
            line = lines[i]
            m = p.match(line)
            if m:
                lines[i:i + 1] = ['', lines[i], '']
                i += 1
            i += 1
        return lines
