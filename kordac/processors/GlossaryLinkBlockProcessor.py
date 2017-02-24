from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import markdown.inlinepatterns
import re


class GlossaryLinkPattern(markdown.inlinepatterns.Pattern):
    occurance_counter = {}

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'glossary-link'
        self.pattern = re.compile(ext.processor_info['glossary-link']['pattern'])
        self.template = ext.jinja_templates['glossary-link']
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):

        # block is a string containing the matched string as a substring
        block = blocks.pop(0)
        match = self.pattern.search(block) # match object

        # get text before and after link
        pattern_pos = match.span()
        text_before_link = block[:pattern_pos[0]]
        text_after_link = block[pattern_pos[1]:]

        # get the string for the glossary link only
        whole_glossary_string = match.group()
        # should really be doing this with parse_argument() (for example) (i.e. not regex)
        term = re.search(r'term="(.*?)"', whole_glossary_string).group(1)
        term = term.lower().replace(' ', '-')

        # check if term has appeared previously
        if term in self.occurance_counter:
            self.occurance_counter[term] += 1
        else:
            self.occurance_counter[term] = 1

        id_count = term + '-' + str(self.occurance_counter[term])

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
