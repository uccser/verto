import re
from markdown.util import etree
from kordac.processors.errors.ArgumentMissingError import ArgumentMissingError

def parse_argument(argument_key, arguments, default=None):
    """Search for the given argument in a string of all arguments
    Returns: Value of an argument as a string if found, otherwise None"""
    result = re.search(r'(^|\s+){}="([^"]*("(?<=\\")[^"]*)*)"'.format(argument_key), arguments)
    if result:
        argument_value = result.group(2)
    else:
        argument_value = default
    return argument_value

def parse_flag(argument_key, arguments, default=False):
    """Search for the given argument in a string of all arguments
    Returns: Value of an argument as a string if found, otherwise None"""
    result = re.search(r'(^|\s+){}($|\s)'.format(argument_key), arguments)
    if result:
        argument_value = True
    else:
        argument_value = default
    return argument_value

def check_arguments(processor, inputs, arguments):
    '''
    Raises an error if the arguments are missing any required parameters or a parameter an optional parameter is dependent on.
    '''
    for argument, argument_info in arguments.items():
        is_required = argument_info['required']
        is_arg = parse_argument(argument, arguments, None) is not None
        is_flag = parse_flag(argument, arguments)

        if is_required and (is_arg or is_flag):
            raise ArgumentMissingError(processor, parameter, "{} is a required argument.".format(argument))
        elif not is_required and (is_arg or is_flag):
            dependencies = argument_info['dependencies']
            for other_argument in dependencies:
                if not (parse_argument(other_argument, arguments, None) is None
                    or parse_flag(other_argument, arguments) is None):
                        raise ArgumentMissingError(processor, argument, "{} is a required parameter because {} exists.".format(other_argument, argument))

def find_transformation(option):
    '''
    Returns a transformation for a given string.
    In future should be able to combine piped transformations into a single
    function.
    '''
    return {
        'str.lower': lambda x: x.lower(),
        'str.upper': lambda x: x.upper(),
    }.get(option, None)

def blocks_to_string(blocks):
    """Returns a string after the blocks have been joined back together."""
    return '\n\n'.join(blocks).rstrip('\n')

def centre_html(node, width):
    """Wraps the given node with HTML to centre using the given number of columns"""
    offset_width = (12 - width) // 2
    root = etree.fromstring(CENTERED_HTML.format(width=width, offset_width=offset_width))
    root.find(".//div[@content]").append(node)
    return root
