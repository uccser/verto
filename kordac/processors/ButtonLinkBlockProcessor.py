from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument, check_required_parameters, check_optional_parameters
import re
from markdown.util import etree

class ButtonLinkBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'button-link'
        self.template = ext.jinja_templates[self.processor]
        self.relative_file_template = ext.jinja_templates['relative-file-link']
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        match = self.pattern.search(block)

        arguments = match.group('args')
        context = dict()
        context['link'] = parse_argument('link', arguments)
        context['text'] = parse_argument('text', arguments)
        context['file'] = parse_argument('file', arguments, 'no').lower() == 'yes'

        check_required_parameters(self.processor, self.required_parameters, context)
        check_optional_parameters(self.processor, self.optional_parameters, context)

        if context['file']:
            context['link'] = self.relative_file_template.render({'file_path': context['link']})

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
