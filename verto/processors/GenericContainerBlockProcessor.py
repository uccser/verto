from markdown.blockprocessors import BlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.processors.utils import etree, parse_arguments, process_parameters, blocks_to_string
from verto.utils.HtmlParser import HtmlParser
from verto.utils.HtmlSerializer import HtmlSerializer
import re


class GenericContainerBlockProcessor(BlockProcessor):
    def __init__(self, processor, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = processor
        self.p_start = re.compile(r'(^|\n) *\{{{0} ?(?P<args>[^\}}]*)(?<! end)\}} *(\n|$)'.format(self.processor))
        self.p_end = re.compile(r'(^|\n) *\{{{0} end\}} *(\n|$)'.format(self.processor))
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info.get('template_name', self.processor)
        self.template = ext.jinja_templates[template_name]
        self.template_parameters = ext.processor_info[self.processor].get('template_parameters', None)
        self.process_parameters = lambda processor, parameters, argument_values: \
            process_parameters(ext, processor, parameters, argument_values)
        self.blocks = None
        self.block = None
        self.start_tag = None
        self.end_tag = None
        self.argument_values = None
        self.the_rest = ''
        self.content_blocks = []
        self.parent = None
        self.inner_start_tags = 0
        self.inner_end_tags = 0

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            block: The block to be tested.

        Returns:
            True if there are any start or end tags within the block.
        '''
        return self.p_start.search(block) is not None or self.p_end.search(block) is not None

    def run(self, parent, blocks):
        ''' Generic run method for container tags.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            blocks: A list of strings of the document, where the
                first block tests true.
        '''
        self.blocks = blocks
        self.block = self.blocks.pop(0)
        self.parent = parent
        self.start_tag = self.p_start.search(self.block)
        self.end_tag = self.p_end.search(self.block)

        self.get_content()
        self.custom_parsing()
        self.convert_to_html()

    def get_content(self):
        '''Get arguments and content of block
        '''
        if ((self.start_tag is None and self.end_tag is not None)
           or (self.start_tag and self.end_tag and self.start_tag.end() > self.end_tag.start())):
            raise TagNotMatchedError(self.processor, self.block, 'end tag found before start tag')

        before = self.block[:self.start_tag.start()]
        after = self.block[self.start_tag.end():]

        if before.strip() != '':
            self.parser.parseChunk(self.parent, before)
        if after.strip() != '':
            self.blocks.insert(0, after)

        self.argument_values = parse_arguments(self.processor, self.start_tag.group('args'), self.arguments)

        self.content_blocks = []
        self.the_rest = ''
        self.inner_start_tags = 0
        self.inner_end_tags = 0

        while len(self.blocks) > 0:
            self.block = self.blocks.pop(0)
            inner_tag = self.p_start.search(self.block)
            self.end_tag = self.p_end.search(self.block)

            if ((inner_tag and self.end_tag is None)
               or (inner_tag and self.end_tag and inner_tag.start() < self.end_tag.end())):
                self.inner_start_tags += 1

            if self.end_tag and self.inner_start_tags == self.inner_end_tags:
                self.content_blocks.append(self.block[:self.end_tag.start()])
                self.the_rest = self.block[self.end_tag.end():]
                break
            elif self.end_tag:
                self.inner_end_tags += 1
                self.end_tag = None
            self.content_blocks.append(self.block)

        if self.the_rest.strip() != '':
            self.blocks.insert(0, self.the_rest)

        if self.end_tag is None or self.inner_start_tags != self.inner_end_tags:
            raise TagNotMatchedError(self.processor, self.block, 'no end tag found to close start tag')

    def custom_parsing(self):
        '''Method to be overriden by processors using GenericContainerBlockProcessor
           but require further parsing of the content
        '''
        pass

    def convert_to_html(self):
        '''Convert the content to html element and render in template
        '''

        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, blocks_to_string(self.content_blocks))

        content = ''
        for child in content_tree:
            content += HtmlSerializer.tostring(child) + '\n'
        content = content.strip('\n')

        if content.strip() == '':
            message = 'content cannot be blank.'
            raise ArgumentValueError(self.processor, 'content', content, message)

        self.argument_values['content'] = content
        context = self.process_parameters(self.processor, self.template_parameters, self.argument_values)

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        self.parent.append(parser.get_root())
