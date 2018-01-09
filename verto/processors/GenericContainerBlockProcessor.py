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
        tag_argument = ext.processor_info[self.processor].get('tag_argument', self.processor)
        self.p_start = re.compile(r'(^|\n) *\{{{0} ?(?P<args>[^\}}]*)(?<! end)\}} *(\n|$)'.format(tag_argument))
        self.p_end = re.compile(r'(^|\n) *\{{{0} end\}} *(\n|$)'.format(tag_argument))
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info[self.processor].get('template_name', self.processor)
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

        Raises:
            ArgumentValueError: If value for a given argument is incorrect.
            TagNotMatchedError: If end tag is not found for corresponding start tag.
        '''
        block = blocks.pop(0)

        start_tag = self.p_start.search(block)
        end_tag = self.p_end.search(block)

        if ((start_tag is None and end_tag is not None) or
           (start_tag and end_tag and start_tag.end() > end_tag.start())):
            raise TagNotMatchedError(self.processor, block, 'end tag found before start tag')

        before = block[:start_tag.start()]
        after = block[start_tag.end():]

        if before.strip() != '':
            self.parser.parseChunk(parent, before)
        if after.strip() != '':
            blocks.insert(0, after)

        argument_values = parse_arguments(self.processor, start_tag.group('args'), self.arguments)

        content_blocks = []
        the_rest = ''
        inner_start_tags = 0
        inner_end_tags = 0

        while len(blocks) > 0:
            block = blocks.pop(0)
            inner_tag = self.p_start.search(block)
            end_tag = self.p_end.search(block)

            if ((inner_tag and end_tag is None) or (inner_tag and end_tag and inner_tag.start() < end_tag.end())):
                inner_start_tags += 1

            if end_tag and inner_start_tags == inner_end_tags:
                content_blocks.append(block[:end_tag.start()])
                the_rest = block[end_tag.end():]
                break
            elif end_tag:
                inner_end_tags += 1
                end_tag = None
            content_blocks.append(block)

        content_blocks, extra_args = self.custom_parsing(content_blocks, argument_values)
        argument_values.update(extra_args)

        if the_rest.strip() != '':
            blocks.insert(0, the_rest)

        if end_tag is None or inner_start_tags != inner_end_tags:
            raise TagNotMatchedError(self.processor, block, 'no end tag found to close start tag')

        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, blocks_to_string(content_blocks))

        content = ''
        for child in content_tree:
            content += HtmlSerializer.tostring(child) + '\n'
        content = content.strip('\n')

        if content.strip() == '':
            message = 'content cannot be blank.'
            raise ArgumentValueError(self.processor, 'content', content, message)

        argument_values['content'] = content
        context = self.process_parameters(self.processor, self.template_parameters, argument_values)

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())

    def custom_parsing(self, content_blocks, argument_values):
        '''
        This serves as a placeholder method, to be used by processes that use the
        GenericContainerBlockProcessor but need to carry out further parsing of
        the block's contents.

        Args:
            content_blocks: List of strings to either be parsed or inserted as content in template.
            argument_values: Dictionary of values to be inserted in template.
        Returns:
            Tuple containing content_blocks (unchanged) and empty dictionary.
        '''
        return (content_blocks, {})
