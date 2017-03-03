from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re

class TableOfContentsBlockProcessor(BlockProcessor):
    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
            reside in.
            args: Arguments handed to the super class.
            kwargs: Arguments handed to the super class.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'table-of-contents'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Processes the block matching the heading and adding to the
        html tree and the kordac heading tree.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            blocks: A list of strings of the document, where the
            first block tests true.
        '''
        block = blocks.pop(0)
        match = self.pattern.search(block)

        html_string = self.template.render(dict())
        node = etree.fromstring(html_string)
        parent.append(node)
