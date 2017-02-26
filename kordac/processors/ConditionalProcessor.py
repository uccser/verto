from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import blocks_to_string, parse_argument, parse_flag, etree, check_required_parameters, check_optional_parameters
import kordac.processors.errors.TagNotMatchedError as TagNotMatchedError
import re

class ConditionalProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'conditional'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.p_end = re.compile(ext.processor_info[self.processor]['pattern_end'])

        self.template = ext.jinja_templates[self.processor]
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        return self.pattern.search(block) is not None or self.p_end.search(block) is not None

    def get_content(self, blocks):
        '''
        next_tag will be None if reached the end.
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
            end_tag = self.p_end.search(block)

            is_if = next_tag is not None and parse_flag('if', next_tag.group('args'))
            is_elif = next_tag is not None and parse_flag('elif', next_tag.group('args'))
            is_else = next_tag is not None and parse_flag('else', next_tag.group('args'))

            # Keep track of how many inner boxed-text start tags we have seen
            if is_if:
                inner_if_tags += 1

            if inner_if_tags != inner_end_tags:
                if end_tag is not None:
                    inner_end_tags += 1
                    end_tag = None
            elif is_elif or is_else or end_tag is not None:
                content_blocks.append(block[:end_tag.start()])
                the_rest = block[end_tag.end():]
                break
            content_blocks.append(block)

        if the_rest:
            blocks.insert(0, the_rest) # Keep anything off the end, should be empty though

        if inner_if_tags != inner_end_tags:
            raise TagNotMatchedError(self.processor, block, 'no end tag found to close start tag')

        return next_tag, content_blocks[:-1]

    def parse_blocks(self, blocks):
        # Parse all the inner content of the boxed-text tags
        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, blocks_to_string(blocks))

        # Convert parsed element tree back into html text for rendering
        content = ''
        for child in content_tree:
            content += etree.tostring(child, encoding="unicode", method="html") + '\n'
        return content

    def run(self, parent, blocks):
        block = blocks.pop(0)
        context = dict()

        start_tag = self.pattern.search(block)
        end_tag = self.p_end.search(block)

        # Found an end tag without processing a start tag first
        if start_tag is None and end_tag is not None:
            raise TagNotMatchedError(self.processor, block, 'end tag found before start tag')

        is_if = parse_flag('if', start_tag.group('args'))

        # elif or else before an if conditional
        if not is_if:
            is_elif = parse_flag('elif', start_tag.group('args'))
            is_else = parse_flag('else', start_tag.group('args'))
            msg = '{} conditional found before if'.format('elif' if is_elif else 'else' if is_else else 'unrecognised')
            raise TagNotMatchedError(self.processor, block, msg)

        # Put left overs back on blocks, should be empty though
        blocks.insert(0, block[start_tag.end():])

        # Process if statement
        if_expression = parse_argument('condition', start_tag.group('args'))
        next_tag, content_blocks = self.get_content(blocks)
        if_content = self.parse_blocks(content_blocks)

        context['if_expression'] = if_expression
        context['if_content'] = if_content

        # Process elif statements
        elifs = dict()
        while next_tag is not None and parse_flag('elif', next_tag.group('args')):
            elif_expression = parse_argument('condition', next_tag.group('args'))
            blocks.insert(0, block[next_tag.end():])
            next_tag, content_blocks = self.get_content(blocks)
            content = self.parse_blocks(content_blocks)
            elifs[elif_expression] = content
        context['elifs'] = elifs

        # Process else statement
        has_else = next_tag is not None and parse_flag('else', next_tag.group('args'))
        else_content = ''
        if has_else:
            blocks.insert(0, block[next_tag.end():])
            next_tag, content_blocks = self.get_content(blocks)
            else_content = self.parse_blocks(content_blocks)
        context['has_else'] = has_else
        context['else_content'] = else_content

        # check_required_parameters(self.processor, self.required_parameters, context)
        # check_optional_parameters(self.processor, self.optional_parameters, context)

        # Render template and compile into an element
        html_string = self.template.render(context)
        print(html_string)
        node = etree.fromstring(html_string)

        parent.append(node)
