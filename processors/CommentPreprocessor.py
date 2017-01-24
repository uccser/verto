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

