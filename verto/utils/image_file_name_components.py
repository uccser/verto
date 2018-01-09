"""Splits components of image file path."""

import re
from os.path import splitext


def image_file_name_components(full_file_path):
    """Splits components of image file path.

    Args:
        full_file_path (str): The complete image file path.

    Returns:
        Dictionary of strings for components of file path.
    """
    components = dict()
    file_path_without_ext, file_extension = splitext(full_file_path)
    pattern = re.compile(r'(?P<file_path>[^@]+)(@(?P<file_width_value>\d+)(?P<file_width_unit>.*))?')
    match = pattern.match(file_path_without_ext)
    components['file_path'] = match.group('file_path')
    file_width_value = match.group('file_width_value')
    if file_width_value:
        components['file_width_value'] = int(file_width_value)
        components['file_width_unit'] = match.group('file_width_unit')
    components['file_extension'] = file_extension
    return components
