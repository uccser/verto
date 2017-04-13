from markdown.blockprocessors import BlockProcessor
from verto.processors.utils import parse_arguments, process_parameters
from verto.utils.HtmlParser import HtmlParser
import re


class GenericTagBlockProcessor(BlockProcessor):
    ''' A generic processor that matches '{<name> args}' and replaces
    with the according html template.
    '''
    def __init__(self, processor, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = processor
        self.pattern = re.compile(r'(^|\n) *\{{{0} ?(?P<args>[^\}}]*)\}} *(\n|$)'.format(self.processor))
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info.get('template_name', self.processor)
        self.template = ext.jinja_templates[template_name]
        self.template_parameters = ext.processor_info[self.processor].get('template_parameters', None)
        self.process_parameters = lambda processor, parameters, argument_values: \
            process_parameters(ext, processor, parameters, argument_values)

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

        argument_values = parse_arguments(self.processor, match.group('args'), self.arguments)
        context = self.process_parameters(self.processor, self.template_parameters, argument_values)

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())
