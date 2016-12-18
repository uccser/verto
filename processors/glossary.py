from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re
import sys


GLOSSARY_TEMPLATE = """
<a href='../further-information/glossary.html#{word}' id='glossary-{occurance}' class='glossary-anchor-link glossary-link-back-reference'>{term}</a>
"""
# P_START = '^\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}.*\{glossary-link end\}'
# P_START = '\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}'
# P_END = '\{glossary-link end\}'

class GlossaryLinkBlockProcessor(BlockProcessor):
    p_start = re.compile('\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}.*\{glossary-link end\}')
    occurance_counter = {'test': 1}

    def test(self, parent, block):
        return self.p_start.search(block) is not None

    def run(self, parent, blocks):

        # block is a string containing the matched string as a substring
        block = blocks.pop(0)
        match = self.p_start.search(block) # match object

        # get text before and after link
        pattern_pos = match.span()
        text_before_link = block[:pattern_pos[0]]
        text_after_link = block[pattern_pos[1]:]

        # get the string for the glossary link only
        whole_glossary_string = match.group()
        term = re.search(r'term="(.*?)"', whole_glossary_string).group(1)
        term = term.lower().replace(' ', '-')

        # check if term has appeared previously
        if term in self.occurance_counter:
            self.occurance_counter[term] += 1
        else:
            self.occurance_counter[term] = 1

        id_count = term + '-' + str(self.occurance_counter[term])

        # build whole sentence including glossary link
        html_string = '<p>'
        html_string += text_before_link
        html_string += GLOSSARY_TEMPLATE.format(word=term, occurance=id_count, term=term)
        html_string += text_after_link
        html_string += '</p>'

        # adds the sentence to the DOM - I think?...
        node = etree.fromstring(html_string)
        parent.append(node)




