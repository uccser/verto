import re
from markdown.util import etree
from collections import OrderedDict
from kordac.processors.errors.ArgumentMissingError import ArgumentMissingError

def parse_argument(argument_key, arguments, default=None):
    ''' Search for the given argument in a string of all arguments

    Args:
        argument_key: The name of the argument.
        arguments: A string of the argument inputs.
        default: The default value if not found.
    Returns:
        Value of an argument as a string if found, otherwise None.
    '''
    result = re.search(r'(^|\s+){}="([^"]*("(?<=\\")[^"]*)*)"'.format(argument_key), arguments)
    if result:
        argument_value = result.group(2)
    else:
        argument_value = default
    return argument_value

def parse_flag(argument_key, arguments, default=False):
    ''' Search for the given argument in a string of all arguments,
    treating the argument as a flag only.

    Args:
        argument_key: The name of the argument.
        arguments: A string of the argument inputs.
        default: The default value if not found.
    Returns:
        Value of an argument as a string if found, otherwise None.
    '''
    result = re.search(r'(^|\s+){}($|\s)'.format(argument_key), arguments)
    if result:
        argument_value = True
    else:
        argument_value = default
    return argument_value

def parse_arguments(processor, inputs, arguments):
    ''' Parses the arguments of a given input and ensures
    they meet the defined requirements.

    Args:
        processor: The processor of the given arguments.
        inputs: A string of the arguments from user input.
        arguments: A dictionary of argument descriptions.
    Returns:
        A dictionary of arguments to values.
    Raises:
        ArgumentMissingError: If any required arguments are missing or
        an argument an optional argument is dependent on is missing.
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
    Processes a given set of arguments by the parameter definitions.

    Args:
        processor: The processor of the given arguments.
        parameters: A dictionary of parameter definitions.
        argument_values: A dictionary of argument to values.
    Returns:
        A dictionary of parameter to converted values.
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
    TODO:
    In future should be able to combine piped transformations
    into a single function.

    Args:
        option: The desired transformations.
    Returns:
        A function of the transformation.
    '''
    return {
        'str.lower': lambda x: x.lower(),
        'str.upper': lambda x: x.upper(),
        'relative_file_link': lambda x: self.relative_file_template.render({'file_path': x})
    }.get(option, None)

def blocks_to_string(blocks):
    ''' Returns a string after the blocks have been joined back together.

    Args:
        blocks: A list of strings of the document blocks.
    Returns:
        A string of the document.
    '''
    return '\n\n'.join(blocks).rstrip('\n')
