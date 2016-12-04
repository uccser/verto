from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re
import sys

GLOSSARY_TEMPLATE = """
<h{heading_level} class='section-heading anchor-link glossary-anchor-link{extra_classes}'><a href='{back_permalink}'>{term}</a></h{heading_level}>
"""
# P_START = '^\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}.*\{glossary-link end\}'
# P_START = '\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}'
# P_END = '\{glossary-link end\}'

class GlossaryLinkBlockProcessor(BlockProcessor):
    p_start = re.compile('^\{glossary-link term="([a-zA-Z]| )*"( reference-text="([a-zA-Z]| )*"){0,1}\}.*\{glossary-link end\}')
    p_end = re.compile('\{glossary-link end\}')


    def test(self, parent, block):
        return self.p_start.match(block) is not None

    def run(self, parent, blocks):
        # f = open('blocks.txt', 'w')
        # for line in blocks:
            # f.write(line)
        block = blocks.pop(0)
        print(block)

        test_string = GLOSSARY_TEMPLATE.format(heading_level="1", extra_classes="", back_permalink="", term="test")
        # print(test_string)

        node = etree.fromstring(test_string)
        parent.append(node)

