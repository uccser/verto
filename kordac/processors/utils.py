import re
from markdown.util import etree
from kordac.processors.errors.ParameterMissingError import ParameterMissingError

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
