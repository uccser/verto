from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
import re


class CommentPreprocessor(Preprocessor):
    # comments contained in one line
    pattern = re.compile('{comment ((?!end)|end)[^}]+\}')

    def test(self, lines):
        return self.pattern.match(lines) is not None

    def run(self, lines):
        # if the comment is contained in the one block, removes the comment from the string
        for i, line in enumerate(lines):
            lines[i] = re.sub(self.pattern, '', line)
        return lines


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
