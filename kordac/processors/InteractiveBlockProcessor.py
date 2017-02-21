from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from kordac.processors.utils import parse_argument, check_required_parameters, check_optional_parameters
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
        name = parse_argument('name', arguments)
        interactive_type = parse_argument('type', arguments)

        if name is not None and name is '':
            raise Error("TODO Proper error")

        if interactive_type == 'in-page':
            self.scripts.append('\n{{% include \'interactive/{}/scripts.html\' %}}\n'.format(name))
        self.required.add(name)

        context = {'name': name, 'type': interactive_type}

        check_required_parameters(self.processor, self.required_parameters, context)
        check_optional_parameters(self.processor, self.optional_parameters, context)

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
