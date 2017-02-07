from markdown.blockprocessors import BlockProcessor
import kordac.processors.utils as utils
import re

class TextBoxBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p_start = re.compile(ext.tag_patterns['text-box']['pattern_start'])
        self.p_end = re.compile(ext.tag_patterns['text-box']['pattern_end'])
        self.template = ext.jinja_templates['text-box']

    def test(self, parent, block):
        return self.p_start.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)

        start_tag = self.p_start.search(block)
        end_tag = None

        blocks.insert(0, block[start_tag.end():])

        content = ""
        the_rest = None

        while len(blocks) > 0:
            block = blocks.pop()
            end_tag = self.p_end.search(block)
            if end_tag:
                content += block[:end_tag.start()]
                the_rest = block[end_tag.end():]
                break
            content += block

        if the_rest:
            blocks.insert(0, the_rest)

        attributes = self.get_attributes(start_tag.group('args'))

        context = dict()
        context.update('indented', True if attributes['indented'] else False)
        context.update('content', content)

        html_string = self.template.format(context)
        node = etree.fromstring(html_string)
        parent.append(node)
