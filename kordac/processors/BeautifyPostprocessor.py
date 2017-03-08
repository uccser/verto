from markdown.postprocessors import Postprocessor
from markdown.util import HtmlStash
from markdown.odict import OrderedDict
from bs4 import BeautifulSoup
import re

class BeautifyPostprocessor(Postprocessor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pre_pattern = re.compile(r'<pre>.*?</pre>', re.DOTALL)
        self.code_pattern = re.compile(r'<code>(?P<code>.*?)</code>', re.DOTALL)
        self.html_stash = HtmlStash()

    def run(self, text):
        text = self.store_non_pre_code_tags(text)
        text = BeautifulSoup(text, 'html.parser').prettify()  # Could use `formatter="html"`
        text = self.restore_non_pre_code_tags(text)
        return text

    def store_non_pre_code_tags(self, text):
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
            html_string = match.group()
            placeholder = self.html_stash.store(html_string, True)
            out_text = text[:match.start()] + placeholder
            text = text[match.end():]
            match = self.pre_pattern.search(text)
        out_text += text

        return out_text

    def restore_non_pre_code_tags(self, text):
        replacements = OrderedDict()
        for i in range(self.html_stash.html_counter):
            html, safe = self.html_stash.rawHtmlBlocks[i]
            replacements[self.html_stash.get_placeholder(i)] = html

        if len(replacements) > 0:
            pattern = re.compile("|".join(re.escape(k) for k in replacements))
            text = pattern.sub(lambda m: replacements[m.group(0)], text)

        return text
