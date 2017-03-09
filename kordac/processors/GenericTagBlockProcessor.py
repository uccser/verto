from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import *
import re

class GenericTagBlockProcessor(BlockProcessor):
    def __init__(self, processor, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Kordac Extension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = processor
        self.pattern = re.compile(r'\{{{0} ?(?P<args>[^\}}]*)\}}').format(self.processor)
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = self.processor['template_name']
        self.template = ext.jinja_templates[ext.processor_info[template_name]
        self.template_parameters = ext.processor_info[self.processor]['template_parameters']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if there is a match within the block.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Generic run method for single match tags.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            blocks: A list of strings of the document, where the
            first block tests true.
        '''
        block = blocks.pop(0)

        match = self.pattern.search(block)
        before = block[:match.start()]
        after = block[match.end():]

        if before.strip() != '':
            self.parser.parseChunk(parent, before)
        if after.strip() != '':
            blocks.insert(0, after)

        if len(self.arguments) > 0:
            check_arguments(self.processor, match.group('args'), self.arguments)

        context = dict()
        for parameter, parameter_info in self.template_parameters.items():
            argument_name = parameter_info['argument']
            parameter_default = parameter_info['default'] if 'default' in parameter_info else None
            argument_value = parse_argument(argument_name, match.group('args'), parameter_default)
            transformation = find_transformation(parameter_info['transform'])
            parameter_value = transformation(argument_value) if transformation is not None else argument_value
            context[parameter] = parameter_value

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
