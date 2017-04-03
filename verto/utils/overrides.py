import re
from markdown.util import string_type

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
