from markdown.preprocessors import Preprocessor

class WhitespacePreprocessor(Preprocessor):
    """Strip extra blank lines between blocks so that only one empty line
    seperates each block
    """
    def run(self, lines):
        count, i = 0, 0
        while i < len(lines):
            line = lines[i]
            if line == '':
                count += 1
                if count > 1:
                    lines.pop(i)
                    continue
            else:
                count = 0
            i += 1
        return lines
