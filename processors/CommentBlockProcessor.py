from markdown.blockprocessors import BlockProcessor
import re

class CommentBlockProcessor(BlockProcessor):
    # comments spread across multiple lines
    p_start = re.compile('^\{comment\}')
    p_end = re.compile('\{comment end\}')

    def test(self, parent, block):
        return self.p_start.match(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        # removes comment blocks from text
        while self.p_end.search(block) is None and len(blocks) > 0:
            block = blocks.pop(0)
