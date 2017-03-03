from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import blocks_to_string, parse_argument, etree, check_argument_requirements
import re

class FrameBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'iframe'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)

        match = self.pattern.search(block)

        check_argument_requirements(self.processor, match.group('args'), self.required_parameters, self.optional_parameters)

        context = dict()
        context['link'] = parse_argument('link', match.group('args'))

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
