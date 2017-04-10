from markdown.blockprocessors import BlockProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.processors.utils import etree, parse_arguments, parse_flag, blocks_to_string
from verto.utils.HtmlParser import HtmlParser
from verto.utils.HtmlSerializer import HtmlSerializer
from collections import OrderedDict
import re


class ConditionalProcessor(BlockProcessor):
    ''' Searches a Document for conditional tags e.g.
    {conditonal flag condition="<condition>"}  The processor matches
    the following `elif` and `else` statements in the document and
    parses them via the provided html template.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the VertoExtension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'conditional'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info.get('template_name', self.processor)
        self.template = ext.jinja_templates[template_name]
        self.template_parameters = ext.processor_info[self.processor].get('template_parameters', None)

    def test(self, parent, block):
        ''' Tests if the block if it contains any type of conditional
        types.

        Args:
            parent: The parent element of the html tree.
            blocks: The markdown blocks to until a new tag is found.
        Returns:
            Return true if any conditional tag is found.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Replaces all conditionals with the given html template.
        Allows for recursively defined if statements.

        Args:
            lines: A list of lines of the Markdown document to be
                converted.
        Returns:
            Markdown document with comments removed.
        Raises:
            TagNotMatchedError: When a condition tags does not have
                a matching start tag, or a start tag does not have
                a matching end tag.
        '''
        block = blocks.pop(0)
        context = dict()

        start_tag = self.pattern.search(block)
        is_if = parse_flag('if', start_tag.group('args'))

        # elif or else before an if conditional
        if not is_if:
            is_elif = parse_flag('elif', start_tag.group('args'))
            is_else = parse_flag('else', start_tag.group('args'))
            is_end = parse_flag('end', start_tag.group('args'))
            string = 'elif' if is_elif else 'else' if is_else else 'end' if is_end else 'unrecognised'
            msg = '{} conditional found before if'.format(string)
            raise TagNotMatchedError(self.processor, block, msg)

        # Put left overs back on blocks, should be empty though
        if block[:start_tag.start()].strip() != '':
            self.parser.parseChunk(parent, block[:start_tag.start()])
        if block[start_tag.end():].strip() != '':
            blocks.insert(0, block[start_tag.end():])

        # Process if statement
        argument_values = parse_arguments(self.processor, start_tag.group('args'), self.arguments)
        if_expression = argument_values['condition']
        next_tag, block, content_blocks = self.get_content(blocks)
        if_content = self.parse_blocks(content_blocks)

        context['if_expression'] = if_expression
        context['if_content'] = if_content

        # Process elif statements
        elifs = OrderedDict()
        while next_tag is not None and parse_flag('elif', next_tag.group('args')):
            argument_values = parse_arguments(self.processor, next_tag.group('args'), self.arguments)
            elif_expression = argument_values['condition']
            next_tag, block, content_blocks = self.get_content(blocks)
            content = self.parse_blocks(content_blocks)
            elifs[elif_expression] = content
        context['elifs'] = elifs

        # Process else statement
        has_else = next_tag is not None and parse_flag('else', next_tag.group('args'))
        else_content = ''
        if has_else:
            argument_values = parse_arguments(self.processor, next_tag.group('args'), self.arguments)
            next_tag, block, content_blocks = self.get_content(blocks)
            else_content = self.parse_blocks(content_blocks)
        context['has_else'] = has_else
        context['else_content'] = else_content

        if (next_tag is None
           or (next_tag is not None and not parse_flag('end', next_tag.group('args')))):
            msg = 'end conditional not found'
            raise TagNotMatchedError(self.processor, block, msg)

        # Render template and compile into an element
        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())

    def get_content(self, blocks):
        ''' Recursively parses blocks into an element tree, returning
        a string of the output.

        Args:
            blocks: The markdown blocks to until a new tag is found.

        Returns:
            The next tag (regex match) the current block (string) and
            the content of the blocks (list of strings).

        Raises:
            TagNotMatchedError: When a sibling conditional is not
                closed.
        '''
        next_tag = None

        content_blocks = []
        the_rest = None

        inner_if_tags = 0
        inner_end_tags = 0

        is_elif, is_else = False, False
        while len(blocks) > 0:
            block = blocks.pop(0)

            # Do we have either a start or end tag
            next_tag = self.pattern.search(block)

            is_if = next_tag is not None and parse_flag('if', next_tag.group('args'))
            is_elif = next_tag is not None and parse_flag('elif', next_tag.group('args'))
            is_else = next_tag is not None and parse_flag('else', next_tag.group('args'))
            is_end = next_tag is not None and parse_flag('end', next_tag.group('args'))

            # Keep track of how many inner boxed-text start tags we have seen
            if is_if:
                inner_if_tags += 1

            if inner_if_tags != inner_end_tags:
                if is_end:
                    inner_end_tags += 1
            elif is_elif or is_else or is_end:
                if block[:next_tag.start()].strip() != '':
                    content_blocks.append(block[:next_tag.start()])
                the_rest = block[next_tag.end():]
                break
            content_blocks.append(block)

        if the_rest and the_rest.strip() != '':
            blocks.insert(0, the_rest)  # Keep anything off the end, should be empty though

        if inner_if_tags != inner_end_tags:
            raise TagNotMatchedError(self.processor, block, 'no end tag found to close start tag')

        return next_tag, block, content_blocks

    def parse_blocks(self, blocks):
        '''Recursively parses blocks into an element tree,
        returning a string of the output.

        Args:
            blocks: The markdown blocks to process.

        Returns:
            A string of the element tree which was created.
        '''
        # Parse all the inner content of the boxed-text tags
        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, blocks_to_string(blocks))

        # Convert parsed element tree back into html text for rendering
        content = ''
        for child in content_tree:
            content += HtmlSerializer.tostring(child)
        return content
