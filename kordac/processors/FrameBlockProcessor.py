from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import blocks_to_string, parse_argument, etree, check_argument_requirements
import re

class FrameBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Kordac Extension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'iframe'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.search(block) is not None

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

        match = self.pattern.search(block)

        check_argument_requirements(self.processor, match.group('args'), self.required_parameters, self.optional_parameters)

        context = dict()
        context['link'] = parse_argument('link', match.group('args'))

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
