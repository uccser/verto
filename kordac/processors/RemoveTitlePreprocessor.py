from markdown.preprocessors import Preprocessor
import re

class RemoveTitlePreprocessor(Preprocessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.pattern = re.compile(ext.processor_patterns['title']['pattern'])

    def test(self, lines):
        return self.pattern.search(lines) is not None

    def run(self, lines):
        """If the title is found on a line, remove the line."""
        title_found = False
        for i, line in enumerate(lines):
            if not title_found and self.pattern.search(line) is not None:
                lines[i] = ''
                title_found = True
        return lines
