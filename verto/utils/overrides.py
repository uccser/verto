'''
Contents in this file makes use and modification of the source code of
the Python Markdown Project and therefore if used must abide by the
licences imposed by that project.

Python Markdown Project
------------------------
LICENCE:

Copyright 2007, 2008 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  - Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
  - Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
  - Neither the name of the nor the names of its contributors may be
    used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE PYTHON MARKDOWN PROJECT ''AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ANY CONTRIBUTORS TO THE
PYTHON MARKDOWN PROJECT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import re
from markdown.blockprocessors import ListIndentProcessor
from markdown.blockprocessors import OListProcessor as DefaultOListProcessor
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
    gathering and processing multiple blocks.
    Example:
        *   Lipsum
            Lorem
            Ipsem
    '''

    ITEM_TYPES = ['li']
    LIST_TYPES = ['ul', 'ol']

    def __init__(self, *args):
        '''Create an IndentProcessor, should be used to override the
        ListIndentProcessor in the markdown.parser.
        '''
        super(IndentProcessor, self).__init__(*args)

    def run(self, parent, blocks):
        ''' Overrides ListIndentProcessor to bulk process all
        blocks of the same indent level.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            blocks: A list of strings of the document, where the
                first block tests true.
        '''
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
        '''Overrides ListIndentProcessor to parse mutliple blocks
        to be added to a list item element.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            blocks: A list of strings of the document, where the
                first block tests true.
        '''
        li = etree.SubElement(parent, 'li')
        self.parser.parseBlocks(li, blocks)


class OListProcessor(DefaultOListProcessor):
    '''Process ordered list blocks. Overrides the built-in
    markdown `OListProcessor` for compatibility with
    verto container tags by forcing single item lists content
    to be processed by the indent processor.
    '''

    def __init__(self, parser):
        '''Create an OListProcessor, should be used to override the
        OListProcessor in the markdown.parser.
        '''
        super(OListProcessor, self).__init__(parser)

    def run(self, parent, blocks):
        ''' Overrides OListProcessor to force the content of single items
        to be processed by the indent processor. This is because the may
        be multiple block container tags.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            blocks: A list of strings of the document, where the
                first block tests true.
        '''
        block = blocks.pop(0)
        items = self.get_items(block)
        sibling = self.lastChild(parent)

        # If we have more than one item we cannot have a container tag
        if len(items) != 1:
            blocks.insert(0, block)
            super(OListProcessor, self).run(parent, blocks)
        # Otherwise we might have a container tag
        else:
            item = items[0]

            # Need to do all the preprocessing the same
            # but don't add anything to the element tree
            if sibling is not None and sibling.tag in self.SIBLING_TAGS:
                lst = sibling
                if lst[-1].text:
                    p = etree.Element('p')
                    p.text = lst[-1].text
                    lst[-1].text = ''
                    lst[-1].insert(0, p)
                lch = self.lastChild(lst[-1])
                if lch is not None and lch.tail:
                    p = etree.SubElement(lst[-1], 'p')
                    p.text = lch.tail.lstrip()
                    lch.tail = ''

            elif parent.tag in ['ol', 'ul']:
                lst = parent
            else:
                lst = etree.SubElement(parent, self.TAG)
                if not self.parser.markdown.lazy_ol and self.STARTSWITH != '1':
                    lst.attrib['start'] = self.STARTSWITH

            # Add to the element tree here based on the structure
            # the IndentProcessor should add content to the element
            if item.startswith(' '*self.tab_length):
                blocks.insert(0, item)
            else:
                etree.SubElement(lst, 'li')
                blocks.insert(0, ' ' * self.tab_length + item)


class UListProcessor(OListProcessor):
    '''Process ordered list blocks. Overrides the built-in
    markdown `UListProcessor` for compatibility with
    verto container tags by forcing single item lists content
    to be processed by the indent processor.
    '''

    TAG = 'ul'

    def __init__(self, parser):
        '''Create an UListProcessor, should be used to override the
        UListProcessor in the markdown.parser.
        '''
        super(UListProcessor, self).__init__(parser)
        # Detect an item (``1. item``). ``group(1)`` contains contents of item.
        self.RE = re.compile(r'^[ ]{0,%d}[*+-][ ]+(.*)' % (self.tab_length - 1))
