import re
from markdown.util import etree
from kordac.processors.errors.ParameterMissingError import ParameterMissingError

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

def check_required_parameters(tag, required_parameters, context):
    """Raises an error if the context is missing any required parameters"""
    if not all(parameter in context.keys() for parameter in required_parameters):
        parameter = next(parameter for parameter in required_parameters if parameter not in context.keys())
        raise ParameterMissingError(tag, parameter, "{} is a required parameter.".format(parameter))

def check_optional_parameters(tag, optional_parameters, context):
    """ Raises an error if the context is missing any parameters that an optional parameter is dependent on.
    """
    for option, dependencies in optional_parameters.items():
        if not all(parameter in context.keys() for parameter in dependencies):
            parameter = next(parameter for parameter in dependencies if parameter not in context.keys())
            raise ParameterMissingError(tag, parameter, "{} is a required parameter because {} exists.".format(parameter, option))

def blocks_to_string(blocks):
    """Returns a string after the blocks have been joined back together."""
    return '\n\n'.join(blocks).rstrip('\n')

def centre_html(node, width):
    """Wraps the given node with HTML to centre using the given number of columns"""
    offset_width = (12 - width) // 2
    root = etree.fromstring(CENTERED_HTML.format(width=width, offset_width=offset_width))
    root.find(".//div[@content]").append(node)
    return root
