from markdown.preprocessors import Preprocessor
import re

class HeadingPreprocessor(Preprocessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.pattern = re.compile(ext.tag_patterns['heading_pre']['pattern'])

    def test(self, lines):
        return self.pattern.search(lines) is not None

    def run(self, lines):
        for line in lines:
            match = self.pattern.search(line)
            if match is not None:
                self.ext.page_heading = match.group(1)
                break
        return lines

