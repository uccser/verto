from markdown.preprocessors import Preprocessor
import re

class SaveTitlePreprocessor(Preprocessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.pattern = re.compile(ext.processor_patterns['title']['pattern'])

    def test(self, lines):
        return self.pattern.search(lines) is not None

    def run(self, lines):
        for line in lines:
            match = self.pattern.search(line)
            if match is not None:
                self.ext.title = match.group(1)
                break
        return lines
