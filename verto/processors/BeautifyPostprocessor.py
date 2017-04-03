from markdown.postprocessors import Postprocessor
from markdown.util import HtmlStash
from markdown.odict import OrderedDict
from bs4 import BeautifulSoup
import re


class BeautifyPostprocessor(Postprocessor):
    ''' Converts the output document into a more asthetically
    pleasing version with more consistent whitespace.
    '''

    def __init__(self, *args, **kwargs):
        ''' Creates a new BeautifyPostprocessor.
        '''
        super().__init__(*args, **kwargs)
        self.pre_pattern = re.compile(r'<pre>.*?</pre>', re.DOTALL)
        self.code_pattern = re.compile(r'<code>(?P<code>.*?)</code>', re.DOTALL)
        self.html_stash = HtmlStash()

    def run(self, text):
        '''Converts the document into a more asthetically
        pleasing version.
        Args:
            text: A string of the document to convert.
        Returns:
            A string of the converted document.
        '''
        text = self.store_non_pre_code_tags(text)
        text = BeautifulSoup(text, 'html.parser').prettify(formatter='html')
        text = self.restore_non_pre_code_tags(text)
        return text

    def store_non_pre_code_tags(self, text):
        '''Stores code tags that are not in pre tags to preserve
        whitespacing, replacing with placeholders.

        Args:
            text: A string of the document to process.
        Returns:
            The document with code blocks replaced with placeholders.
        '''
        prepass_text = text
        pre_spans = []

        match = self.pre_pattern.search(prepass_text)
        while match is not None:
            pre_spans.append(match.span())
            prepass_text = prepass_text[match.end():]
            match = self.pre_pattern.search(prepass_text)

        out_text = ''
        match = self.code_pattern.search(text)
        while match is not None:
            if not any(match.start() in range(*span) or match.end() in range(*span) for span in pre_spans):
                html_string = match.group()
                placeholder = self.html_stash.store(html_string, True)
                out_text = text[:match.start()] + placeholder
            else:
                out_text = text[:match.end()]
            text = text[match.end():]
            match = self.pre_pattern.search(text)
        out_text += text

        return out_text

    def restore_non_pre_code_tags(self, text):
        '''Restores code tags that are not in pre tags by replacing
         placeholders. This is to preserve whitespacing.

        Args:
            text: A string of the document to process.
        Returns:
            The document with placeholders replaced with stored
            code blocks.
        '''
        replacements = OrderedDict()
        for i in range(self.html_stash.html_counter):
            html, safe = self.html_stash.rawHtmlBlocks[i]
            replacements[self.html_stash.get_placeholder(i)] = html

        if len(replacements) > 0:
            pattern = re.compile('|'.join(re.escape(k) for k in replacements))
            text = pattern.sub(lambda m: replacements[m.group(0)], text)

        return text
