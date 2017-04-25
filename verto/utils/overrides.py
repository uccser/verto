import re
from markdown.blockprocessors import ListIndentProcessor
from markdown.util import string_type, etree

BLOCK_LEVEL_ELEMENTS = [
    'address', 'article', 'aside', 'blockqoute', 'br', 'canvas', 'dd', 'div',
    'dl', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h[1-6]',
    'header', 'hr', 'li', 'main', 'nav', 'noscript', 'ol', 'output', 'p',
    'pre', 'section', 'table', 'tfoot', 'ul', 'video', 'remove'
]  # TODO: TO MAKE CONFIGURABLE


def is_block_level(html, block_level_elements):
    '''
    Checks if the root element (or first element) of the given
    html is a block level element.
    Args:
        html: A string of the html to check.
        block_level_elements: A list of strings which are the
        block level elements.
    Returns:
        True if the first element is a block level element.
    '''
    m = re.match(r'^\<\/?([^ >]+)', html)
    if m:
        tag = m.group(1)
        if tag[0] in ('!', '?', '@', '%'):
            return True
        if isinstance(tag, string_type):
            elements = '|'.join(block_level_elements)
            block_elements_re = re.compile('^({})$'.format(elements),
                                           re.IGNORECASE)
            return block_elements_re.match(tag)
        return False
    return False


class IndentProcessor(ListIndentProcessor):
    ''' Process children of list items. Overrides the built-in
    markdown `ListIndentProcessor` for compatibility by
    gathering and processing .
    Example:
        *   Lipsum
            Lorem
            Ipsem
    '''

    ITEM_TYPES = ['li']
    LIST_TYPES = ['ul', 'ol']

    def __init__(self, *args):
        super(IndentProcessor, self).__init__(*args)

    def run(self, parent, blocks):
        block = blocks.pop(0)
        level, sibling = self.get_level(parent, block)

        indent_blocks = [self.looseDetab(block, level)]
        while len(blocks) > 0:
            block = blocks.pop(0)
            if self.test(parent, block):
                # Check that block is the same indent_level
                current_level, current_sibling = self.get_level(parent, block)
                if current_level != level and current_sibling != sibling:
                    blocks.insert(0, block)
                    break
                indent_blocks.append(self.looseDetab(block, level))
            # Allow blank blocks within indent
            elif block.strip() != '':
                blocks.insert(0, block)
                break

        self.parser.state.set('detabbed')
        if parent.tag in self.ITEM_TYPES:
            if len(parent) and parent[-1].tag in self.LIST_TYPES:
                self.parser.parseBlocks(parent[-1], indent_blocks)
            else:
                self.parser.parseBlocks(parent, indent_blocks)
        elif sibling.tag in self.ITEM_TYPES:
            self.parser.parseBlocks(sibling, indent_blocks)
        elif len(sibling) and sibling[-1].tag in self.ITEM_TYPES:
            if sibling[-1].text:
                p = etree.Element('p')
                p.text = sibling[-1].text
                sibling[-1].text = ''
                sibling[-1].insert(0, p)
            self.parser.parseBlocks(sibling[-1], indent_blocks)
        else:
            self.create_item(sibling, indent_blocks)
        self.parser.state.reset()

    def create_item(self, parent, blocks):
        """ Create a new li and parse the block with it as the parent. """
        li = util.etree.SubElement(parent, 'li')
        self.parser.parseBlocks(li, blocks)
