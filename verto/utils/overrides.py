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
from math import floor

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

class OListProcessor(DefaultOListProcessor):
    '''Process ordered list blocks. Overrides the built-in
    markdown `OListProcessor` for compatibility with
    verto container tags by forcing single item lists content
    to be processed by the indent processor.
    '''

    LIST_TYPES = ['ul', 'ol']

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
        items = self.get_items(blocks)
        sibling = self.lastChild(parent)

    def get_items(self, blocks):
        """ Break a block into list items. """
        relevant_block_groups = []
        while len(blocks) > 0:
            block = blocks.pop(0)
            if bool(self.RE.match(block)):
                relevant_block_groups.append([])
            elif not (block.startswith(' ' * self.tab_length)
               or block.strip() == ''):
                    blocks.insert(0, block)
                    break
            relevant_block_groups[-1].append(block)

        print(relevant_block_groups)
        items = []
        for block_group in relevant_block_groups:
            if len(block_group) <= 0:
                continue

            block = block_group[-1]
            for line in block.split('\n'):
                m = self.CHILD_RE.match(line)
                if m:
                    # This is a new list item
                    # Check first item for the start index
                    if not items and self.TAG == 'ol':
                        # Detect the integer value of first list item
                        INTEGER_RE = re.compile('(\d+)')
                        self.STARTSWITH = INTEGER_RE.match(m.group(1)).group()
                    # Append to the list
                    items.append(m.group(3))
                elif self.INDENT_RE.match(line):
                    # This is an indented (possibly nested) item.
                    if items[-1].startswith(' '*self.tab_length):
                        # Previous item was indented. Append to that item.
                        items[-1] = '%s\n%s' % (items[-1], line)
                    else:
                        items.append(line)
                else:
                    # This is another line of previous item. Append to that item.
                    items[-1] = '%s\n%s' % (items[-1], line)
        print(items)
        return items


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
