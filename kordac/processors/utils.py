import re
from markdown.util import etree

CENTERED_HTML = """
<div class='row'>
  <div content='' class='content col s12 m{width} offset-m{offset_width} center-align'>
  </div>
</div>
"""

def parse_argument(argument_key, arguments, default=None, convert_type=True):
    """Search for the given argument in a string of all arguments
    Returns: Value of an argument as a string if found, otherwise None"""
    result = re.search(r'(^|\s+){}="([^"]*("(?<=\\")[^"]*)*)"'.format(argument_key), arguments)
    if result:
        argument_value = string_to_type(result.group(2)) if convert_type else result.group(2)
    else:
        argument_value = default
    return argument_value

def string_to_type(string):
    try:
        if re.match("^(-)?\d+?$", string):
            return int(string)
        elif re.match("^(-)?\d+?\.\d+?$", string) is not None:
            return float(string)
        elif string.lower() == 'true' or string.lower() == 'yes':
            return True
        elif string.lower() == 'false' or string.lower() == 'no':
            return False
    except ValueError:
        pass
    return string

def from_kebab_case(text):
    """Returns given kebab case text to plain text.
    Text is camel case, with dashs replaced with spaces
    """
    return text.replace('-', ' ').title()

def to_kebab_case(text):
    """Returns the given text as kebab case.
    The text is lower case, has spaces replaced as dashes.
    All punctuation is also removed.
    """
    text = ''.join(letter for letter in text if letter in set(string.ascii_letters + string.digits + ' -'))
    text = text.replace(' ', '-').lower()
    return text

def blocks_to_string(blocks):
    """Returns a string after the blocks have been joined back together."""
    return '\n\n'.join(blocks)

def centre_html(node, width):
    """Wraps the given node with HTML to centre using the given number of columns"""
    offset_width = (12 - width) // 2
    root = etree.fromstring(CENTERED_HTML.format(width=width, offset_width=offset_width))
    root.find(".//div[@content]").append(node)
    return root
