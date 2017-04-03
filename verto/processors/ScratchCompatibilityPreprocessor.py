from markdown.preprocessors import Preprocessor
import re

# Enable support for | so that languages can be passed options
FENCED_BLOCK_RE_OVERRIDE = re.compile(r'''(?P<fence>^(?:~{3,}|`{3,}))[ ]*
(\{?\.?(?P<lang>[\w#.+-:]*))?[ ]*
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)


class ScratchCompatibilityPreprocessor(Preprocessor):
    '''Should only be active if using the scratch processor and the
    extensions for fenced_code and codehilite. This preprocessor works
    similar to the fenced_code preprocessor but only removes scratch
    codeblocks and leaves modification to the downstream processors.

    Uses a similar regex as per the fenced_code extension, and the
    same html escaping of code.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'scratch-compatibility'

        self.pattern = re.compile(ext.processor_info['scratch'][self.processor]['pattern'], re.DOTALL | re.MULTILINE)
        self.CODE_FORMAT = '<pre><code class="scratch{1}">{0}</code></pre>'

    def run(self, lines):
        ''' Inherited from Preprocessor, removes scratch codeblocks
        and stores them for later processing by the scratch block
        processor.

        Args:
            lines: A list of lines of the Markdown document to be converted.
        Returns:
            Markdown document with scratch codeblocks removed.
        '''
        text = '\n'.join(lines)
        match = self.pattern.search(text)
        while match is not None:
            code = self.CODE_FORMAT.format(self._escape(match.group('code')), match.group('options'))
            placeholder = self.markdown.htmlStash.store(code, safe=True)
            text = text[:match.start()] + '\n' + placeholder + '\n' + text[match.end():]
            match = self.pattern.search(text)
        return text.split('\n')

    def _escape(self, text):
        ''' basic html escaping, as per fenced_code.

        Args:
            text: The text to escape.
        Returns:
            An escaped string of text.
        '''
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        return text
