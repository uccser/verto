from markdown.blockprocessors import BlockProcessor
import re

class CommentBlockProcessor(BlockProcessor):
    # comments spread across multiple lines

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p_start = re.compile(ext.tag_patterns['comment_block']['pattern_start'])
        self.p_end = re.compile(ext.tag_patterns['comment_block']['pattern_end'])

    def test(self, parent, block):
        return self.p_start.search(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        # removes comment blocks from text
        print('block', block)
        print(self.p_end.search(block))
        while self.p_end.search(block) is None and len(blocks) > 0:
            print('here')
            block = blocks.pop(0)
