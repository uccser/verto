from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument, etree

import kordac.processors.errors.TagNotMatchedError as TagNotMatchedError
import re

class BoxedTextBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = 'boxed-text'
        self.p_start = re.compile(ext.tag_patterns[self.tag]['pattern_start'])
        self.p_end = re.compile(ext.tag_patterns[self.tag]['pattern_end'])
        self.template = ext.jinja_templates[self.tag]

    def test(self, parent, block):
        return self.p_start.search(block) is not None or self.p_end.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)

        start_tag = self.p_start.search(block)
        end_tag = self.p_end.search(block)

        if start_tag is None and end_tag is not None:
            raise TagNotMatchedError(self.tag, block, 'end tag found before start tag')

        blocks.insert(0, block[start_tag.end():])

        content = ''
        the_rest = None
        inner_start_tags = 0
        inner_end_tags = 0

        while len(blocks) > 0:
            block = blocks.pop(0)

            inner_tag = self.p_start.search(block)
            end_tag = self.p_end.search(block)
            if inner_tag:
                inner_start_tags += 1

            if end_tag and inner_start_tags == inner_end_tags:
                content += block[:end_tag.start()] + '\n\n'
                the_rest = block[end_tag.end():]
                break
            elif end_tag:
                inner_end_tags += 1
                end_tag = None
            content += block + '\n\n'

        if the_rest:
            blocks.insert(0, the_rest)
        if end_tag is None or inner_start_tags != inner_end_tags:
            raise TagNotMatchedError(self.tag, block, 'no end tag found to close start tag')

        content_tree = etree.Element('content')
        self.parser.parseChunk(content_tree, content)

        content = ''
        for child in content_tree:
            content += etree.tostring(child, encoding="unicode", method="html") + '\n'

        context = dict()
        context['indented'] = parse_argument('indented', start_tag.group('args'), False)
        context['text'] = content

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
