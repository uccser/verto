import re
from markdown.util import etree  # noqa: F401
from collections import OrderedDict, defaultdict
from verto.errors.ArgumentDefinitionError import ArgumentDefinitionError
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.ArgumentValueError import ArgumentValueError


def parse_argument(argument_key, arguments, default=None):
    '''Search for the given argument in a string of all arguments

    Args:
        argument_key: The name of the argument.
        arguments: A string of the argument inputs.
        default: The default value if not found.
    Returns:
        Value of an argument as a string if found, otherwise None.
    '''
    is_argument = re.search(r'(^|\s+){}='.format(argument_key), arguments)
    if not is_argument:
        return default

    result = re.match(r'(^|\s+){}="([^"]*("(?<=\\")[^"]*)*)"'.format(argument_key), arguments[is_argument.start():])

    if is_argument and result is None:
        msg = "Argument found but value not contained in double quotes."
        raise ArgumentDefinitionError(argument_key, msg)

    if result:
        argument_value = result.group(2).replace(r'\"', r'"')
        return argument_value
    else:
        return default


def parse_flag(argument_key, arguments, default=False):
    '''Search for the given argument in a string of all arguments,
    treating the argument as a flag only.

    Args:
        argument_key: The name of the argument.
        arguments: A string of the argument inputs.
        default: The default value if not found.
    Returns:
        True if argument is found, otherwise None.
    '''
    result = re.search(r'(^|\s+){}(.+?".*?")'.format(argument_key), arguments)
    if result:
        return True
    else:
        return default


def parse_arguments(processor, inputs, arguments):
    '''Parses the arguments of a given input and ensures
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
    argument_values = defaultdict(None)
    for argument, argument_info in arguments.items():
        is_required = argument_info['required']
        is_arg = parse_argument(argument, inputs, None) is not None  # True if in line

        if is_required and not is_arg:  # required argument and not in line
            raise ArgumentMissingError(processor, argument, '{} is a required argument.'.format(argument))
        elif not is_required and is_arg:
            dependencies = argument_info.get('dependencies', [])
            for other_argument in dependencies:
                if (parse_argument(other_argument, inputs, None) is None and
                   parse_flag(other_argument, inputs, None) is None):
                        message = '{} is a required argument because {} exists.'.format(other_argument, argument)
                        raise ArgumentMissingError(processor, argument, message)

        if is_arg:
            value = parse_argument(argument, inputs, None)
            if value and value.strip() == '':
                message = '{} cannot be blank.'.format(argument)
                raise ArgumentValueError(processor, argument, value, message)
            if argument_info.get('values', None) and value not in argument_info['values']:
                message = '{} is not one of {}.'.format(value, argument_info['values'])
                raise ArgumentValueError(processor, argument, value, message)
            argument_values[argument] = value
    return argument_values


def process_parameters(ext, processor, parameters, argument_values):
    '''Processes a given set of arguments by the parameter definitions.

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
        parameter_default = parameter_info.get('default', None)
        argument_value = argument_values.get(argument_name, parameter_default)

        parameter_value = argument_value
        if parameter_info.get('transform', None):
            transform = find_transformation(ext, parameter_info['transform'])
            if parameter_info.get('transform_condition', None):
                transformations[parameter] = (eval(parameter_info['transform_condition']), transform)
            else:
                transformations[parameter] = (True, transform)

        context[parameter] = parameter_value

    for parameter, (condition, transform) in transformations.items():
        if context[parameter] is not None:
            if isinstance(condition, bool) and condition:
                context[parameter] = transform(context[parameter])
            if callable(condition) and condition(context):
                context[parameter] = transform(context[parameter])
    return context


def find_transformation(ext, option):
    '''Returns a transformation for a given string.
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
        'relative_file_link': lambda x: ext.jinja_templates['relative-file-link'].render({'file_path': x})
    }.get(option, None)


def blocks_to_string(blocks):
    '''Returns a string after the blocks have been joined back
    together.

    Args:
        blocks: A list of strings of the document blocks.
    Returns:
        A string of the document.
    '''
    return '\n\n'.join(blocks).rstrip('\n')
