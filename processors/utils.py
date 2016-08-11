import re

def parse_argument(argument_key, arguments):
    """Search for the given argument in a string of all arguments
    Returns: Value of an argument as a string if found, otherwise None"""
    result = re.search('{}="([^"]*)"'.format(argument_key), arguments)
    if result:
        argument_value = result.group(1)
    else:
        argument_value = None
    return argument_value

def from_kebab_case(text):
    """Returns given kebab case text to plain text.
    Text is camel case, with dashs replaced with spaces
    """
    return text.replace('-', ' ').title()
