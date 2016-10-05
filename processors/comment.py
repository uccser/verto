from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from markdown.util import etree
import re

class CommentPreprocessor(Preprocessor):
    p = re.compile('{comment ((?!end)|end)[^}]+\}')

    def run(self, lines):
        for i, line in enumerate(lines):
            lines[i] = re.sub(self.p, '', line)
        return lines

class CommentBlockProcessor(BlockProcessor):
    p_start = re.compile('^\{comment\}')
    p_end = re.compile('\{comment end\}')

    def test(self, parent, block):
        return self.p_start.match(block) is not None

    def run(self, parent, blocks):
        block = blocks.pop(0)
        while self.p_end.search(block) is None and len(blocks) > 0:
            block = blocks.pop(0)
