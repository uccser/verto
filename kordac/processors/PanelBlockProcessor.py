from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from kordac.processors.utils import blocks_to_string, parse_argument
import re


class PanelBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'panel'
        self.p_start = re.compile(ext.processor_patterns[self.processor]['pattern_start'])
        self.p_end = re.compile(ext.processor_patterns[self.processor]['pattern_end'])
        self.template = ext.jinja_templates[self.processor]

    def test(self, parent, block):
        return self.p_start.search(block) is not None or self.p_end.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)

        # find start of match and place back in blocks list up to end of match
        start_tag = self.p_start.search(block)
        end_tag = self.p_end.search(block)

        if start_tag is None and end_tag is not None:
            raise TagNotMatchedError(self.processor, block, 'end tag found before start tag')

        blocks.insert(0, block[start_tag.end():])

        # iterate over blocks until find {panel end} block
        content_blocks = []
        the_rest = None
        inner_start_tags = 0
        inner_end_tags = 0

        while len(blocks) > 0:
            block = blocks.pop(0)

            # Do we have either a start or end tag        print("Here")
            inner_tag = self.p_start.search(block)
            end_tag = self.p_end.search(block)

            # Keep track of how many inner boxed-text start tags we have seen
            if inner_tag:
                inner_start_tags += 1

            # If we have an end tag and all inner boxed-text tags have been closed - ~FIN
            if end_tag and inner_start_tags == inner_end_tags:
                content_blocks.append(block[:end_tag.start()])
                the_rest = block[end_tag.end():]
                break
            elif end_tag:
                inner_end_tags += 1
                end_tag = None
            content_blocks.append(block)

        if the_rest:
            blocks.insert(0, the_rest) # Keep anything off the end, should be empty though

        # Error if we reached the end without closing the start tag
        # or not all inner boxed-text tags were closed
        if end_tag is None or inner_start_tags != inner_end_tags:
            raise TagNotMatchedError(self.processor, block, 'no end tag found to close start tag')

        # Parse all the inner content of the boxed-text tags
        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, blocks_to_string(content_blocks))

        # Convert parsed element tree back into html text for rendering
        content = ''
        for child in content_tree:
            content += etree.tostring(child, encoding="unicode", method="html") + '\n'

        context = self.get_attributes(start_tag.group('args'))
        context['content'] = content

        # create panel node and add it to parent element
        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)

    def get_attributes(self, args):
        panel_type = parse_argument('type', args)
        title = parse_argument('title', args)
        subtitle = parse_argument('subtitle', args)
        expanded = parse_argument('expanded', args, default='no', convert_type=False)
        return {
            'type': panel_type,
            'title': title,
            'subtitle': subtitle,
            'expanded': expanded
        }
