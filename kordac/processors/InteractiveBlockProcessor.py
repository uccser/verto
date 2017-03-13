from kordac.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from kordac.processors.errors.InvalidParameterError import InvalidParameterError
from kordac.processors.utils import *
from markdown.util import etree

import re
import os

class InteractiveBlockProcessor(GenericTagBlockProcessor):
    '''Searches a Document for interactive tags:
        e.g. {interactive name='example' type='in-page'}
        These are then replaced with the html template.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Kordac Extension.
        '''
        super().__init__('interactive', ext, *args, **kwargs)
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.relative_file_template = ext.jinja_templates['relative-file-link']
        self.scripts = ext.required_files["page_scripts"]
        self.required = ext.required_files["interactives"]

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.match(block) is not None

    def run(self, parent, blocks):
        ''' Processes the block matching the heading and adding to the
        html tree and the kordac heading tree.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            blocks: A list of strings of the document, where the
            first block tests true.
        '''
        block = blocks.pop(0)

        match = self.pattern.match(block)
        before = block[:match.start()]
        after = block[match.end():]

        if before.strip() != '':
            self.parser.parseChunk(parent, before)
        if after.strip() != '':
            blocks.insert(0, after)

        arguments = match.group('args')
        argument_values = parse_arguments(self.processor, arguments, self.arguments)

        name = argument_values['name']
        interactive_type = argument_values['type']
        text = argument_values['text']
        parameters = argument_values['parameters']

        if name is not None and name is '':
            raise InvalidParameterError(self.processor, "name", "Name parameter must not be an empty string.")

        if interactive_type == 'in-page':
            self.scripts.add('interactive/{}/scripts.html'.format(name))
        self.required.add(name)

        file_path = parse_argument('thumbnail', arguments)
        if file_path is None:
            file_path = "{}/thumbnail.png".format(name)

        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None: # internal image
            self.required.add(file_path)
            file_path = self.relative_file_template.render({'file_path': file_path})

        context = dict()
        context['type'] = interactive_type
        context['name'] = name
        context['text'] = text
        context['parameters'] = parameters
        context['file_path'] = file_path

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
