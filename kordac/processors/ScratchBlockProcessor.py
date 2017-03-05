from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import blocks_to_string, parse_argument, etree
from kordac.processors.errors.TagNotMatchedError import TagNotMatchedError
from collections import namedtuple
from hashlib import sha256
import re

class ScratchData(namedtuple('ScratchData', 'hash, text')):
    ''' Represents data required to make a scratch image.

    Keyword arguments:
        hash: hash of the scratch data
        text: text of the scratch code
    '''

class ScratchBlockProcessor(BlockProcessor):
    ''' Searches a Document for codeblocks with the scratch language.
    These are then processed into the kordac result and hashed for
    another program in the pipeline to retrieve or create into images.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
            reside in.
            args: Arguments handed to the super class.
            kwargs: Arguments handed to the super class.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'scratch'
        self.p_start = re.compile(ext.processor_info[self.processor]['pattern_start'])
        self.p_end = re.compile(ext.processor_info[self.processor]['pattern_end'])
        self.template = ext.jinja_templates[self.processor]
        self.scratch_images = ext.required_files['scratch_images']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.p_start.search(block) is not None

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

        start_tag = self.p_start.search(block)
        blocks.insert(0, block[start_tag.end():])

        content_blocks = []
        the_rest = None

        while len(blocks) > 0:
            block = blocks.pop(0)

            inner_tag = self.p_start.search(block)
            end_tag = self.p_end.search(block)

            if inner_tag:
                raise TagNotMatchedError(self.processor, block,
                            'start tag found before previous tag was closed')

            if end_tag is not None:
                content_blocks.append(block[:end_tag.start()])
                the_rest = block[end_tag.end():]
                break
            content_blocks.append(block)

        if the_rest:
            blocks.insert(0, the_rest)

        if end_tag is None:
            raise TagNotMatchedError(self.processor, block,
                                        'no end tag found to close start tag')

        content = '\n\n'.join(content_blocks)
        content_hash = ScratchBlockProcessor.hash_content(content)

        self.update_required_images(content_hash, content)
        html_string = self.template.render({ 'hash': content_hash })
        node = etree.fromstring(html_string)
        parent.append(node)

    @staticmethod
    def hash_content(text):
        '''Finds the hash of the given text for image retrieval.

        Args:
            text: The text to hash.
        Returns:
            The hash of the text for image retrieval.
        '''
        return sha256(text.encode('utf8'))

    def update_required_images(self, content_hash, text):
        '''Adds the scratch code and hash to the kordac result.

        Args:
            content_hash: The image hash.
            text: The source text of the image.
        '''
        self.scratch_images.append(HeadingNode(hash=content_hash, text=text))
