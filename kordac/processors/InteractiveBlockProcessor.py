from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from kordac.processors.utils import parse_argument, check_argument_requirements
from markdown.util import etree

import re
import os

class InteractiveBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'interactive'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.relative_file_template = ext.jinja_templates['relative-file-link']
        self.scripts = ext.page_scripts
        self.required = ext.required_files["interactives"]
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        return self.pattern.match(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.match(block)

        arguments = match.group('args')
        check_argument_requirements(self.processor, arguments, self.required_parameters, self.optional_parameters)

        name = parse_argument('name', arguments)
        interactive_type = parse_argument('type', arguments)
        text = parse_argument('text', arguments)
        parameters = parse_argument('parameters', arguments)

        if name is not None and name is '':
            raise Error("TODO Proper error")

        if interactive_type == 'in-page':
            self.scripts.append('{{% include \'interactive/{}/scripts.html\' %}}'.format(name))
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
