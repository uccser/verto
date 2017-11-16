from markdown.blockprocessors import BlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.errors.ArgumentValueError import ArgumentValueError
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.processors.utils import etree, parse_arguments, process_parameters, blocks_to_string
from verto.utils.HtmlParser import HtmlParser
from verto.utils.HtmlSerializer import HtmlSerializer
import re


class PanelBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        super().__init__(*args, **kwargs)
        # self.processor = processor
        self.processor = 'panel'
        self.p_start = re.compile(r'(^|\n) *\{{{0} ?(?P<args>[^\}}]*)(?<! end)\}} *(\n|$)'.format(self.processor))
        self.p_end = re.compile(r'(^|\n) *\{{{0} end\}} *(\n|$)'.format(self.processor))
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info.get('template_name', self.processor)
        self.panel_template = ext.jinja_templates[template_name]
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
        '''
        block = blocks.pop(0)

        start_tag = self.p_start.search(block)
        end_tag = self.p_end.search(block)

        if ((start_tag is None and end_tag is not None)
           or (start_tag and end_tag and start_tag.end() > end_tag.start())):
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

            if ((inner_tag and end_tag is None)
               or (inner_tag and end_tag and inner_tag.start() < end_tag.end())):
                inner_start_tags += 1

            if end_tag and inner_start_tags == inner_end_tags:
                content_blocks.append(block[:end_tag.start()])
                the_rest = block[end_tag.end():]
                break
            elif end_tag:
                inner_end_tags += 1
                end_tag = None
            content_blocks.append(block)

        argument = 'title'
        title_r = re.compile(r'(^|\n)# ((\w| )*)(?P<args>)')
        title = title_r.search(content_blocks[0])
        if title:
            argument_values[argument] = title.groups()[1]
        else:
            raise ArgumentMissingError(self.processor, argument, '{} is a required argument.'.format(argument))

        argument = 'subtitle'
        if argument_values.get(argument) == 'true':
            subtitle_r = re.compile(r'(^|\n)## ((\w| )*)(?P<args>)')
            subtitle = subtitle_r.search(content_blocks[1])
            if subtitle:
                argument_values[argument] = subtitle.groups()[1]
                content_blocks = content_blocks[2:]
            else:
                raise ArgumentMissingError(self.processor, argument, '{} is set to "true" but not supplied.'.format(argument))
        elif argument_values.get(argument) == 'false':  # false
            del argument_values[argument]  # delete from argument dict so as to not be included in template
            content_blocks = content_blocks[1:]
        else:
            content_blocks = content_blocks[1:]

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

        html_string = self.panel_template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())
