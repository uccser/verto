import re
from markdown.util import etree
from collections import OrderedDict
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

def parse_arguments(processor, inputs, arguments):
    '''
    Returns a dictionary of argument to value.
    Raises an error if the arguments are missing any required parameters or a parameter an optional parameter is dependent on.
    '''
    argument_values = dict()
    for argument, argument_info in arguments.items():
        is_required = argument_info['required']
        is_arg = parse_argument(argument, arguments, None) is not None
        is_flag = parse_flag(argument, arguments)

        if is_required and (is_arg or is_flag):
            raise ArgumentMissingError(processor, parameter, "{} is a required argument.".format(argument))
        elif not is_required and (is_arg or is_flag):
            dependencies = argument_info.get('dependencies', [])
            for other_argument in dependencies:
                if not (parse_argument(other_argument, arguments, None) is None
                    or parse_flag(other_argument, arguments) is None):
                        raise ArgumentMissingError(processor, argument, "{} is a required parameter because {} exists.".format(other_argument, argument))

        if is_flag:
            argument_values[argument] = True
        elif is_arg:
            argument_values[argument] = parse_argument(argument, arguments, None)

    return argument_values

def process_parameters(processor, parameters, argument_values):
    '''
    Returns a dictionary of parameter to value.
    '''
    context = dict()
    transformations = OrderedDict()
    for parameter, parameter_info in parameters.items():
        argument_name = parameter_info['argument']
        parameter_default = parameter_info['default'] if 'default' in parameter_info else None
        argument_value = argument_values[argument_name] if argument_values[argument_name] is not None else parameter_default

        parameter_value = argument_value
        if parameter_info.get('transform', None):
            transformation = find_transformation(parameter_info['transform'])
            if parameter_info.get('transform_condition', None):
                transformations[parameter] = (eval(parameter_info['transform_condition']), transformation)
            else:
                transformations[parameter] = (True, transformation)

        context[parameter] = parameter_value

    for parameter, (condition, transformation) in transformations.items():
        if isinstance(condition, bool) and condition == True:
            context[parameter] = transform(context[parameter])
        if callable(condition) and condition(context):
            context[parameter] = transform(context[parameter])
    return context

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
