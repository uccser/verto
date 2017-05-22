from markdown.treeprocessors import Treeprocessor
from verto.processors.utils import etree
from verto.utils.HtmlParser import HtmlParser
from verto.utils.HtmlSerializer import HtmlSerializer
from collections import namedtuple
from functools import reduce
from hashlib import sha256
from random import shuffle
import re


class ScratchImageMetaData(namedtuple('ScratchImageMetaData', 'hash, text')):
    ''' Represents data required to make a scratch image.

    Keyword arguments:
        hash: hash of the scratch data
        text: text of the scratch code
    '''


class ScratchTreeprocessor(Treeprocessor):
    ''' Searches a Document for codeblocks with the scratch language.
    These are then processed into the verto result and hashed for
    another program in the pipeline to retrieve or create into images.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
            reside in.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'scratch'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.scratch_images = ext.required_files['scratch_images']
        self.fenced_compatibility = 'fenced_code_block' in ext.compatibility

    def run(self, root):
        ''' Processes the html tree finding code tags where scratch
        code is used and replaces with template html.

        Args:
            root: The root of the document element tree.
        '''
        code_elements = []
        for node in root.iterfind('.//pre'):  # A modified tree will leave the iterator undefined.
            code_elements.append(node)

        for node in code_elements:
            self.process_html(node)

        if self.fenced_compatibility:
            for i in range(self.markdown.htmlStash.html_counter):
                html_string, safe = self.markdown.htmlStash.rawHtmlBlocks[i]
                node = None
                try:
                    parser = HtmlParser()
                    node = parser.feed(html_string).close().get_root()
                except etree.ParseError:
                    pass

                if node is None:
                    continue
                self.process_html(node)
                html_string = HtmlSerializer.tostring(node)
                self.markdown.htmlStash.rawHtmlBlocks[i] = html_string, safe

    def process_html(self, node):
        ''' Checks if given node is a scratch code tag and replaces
        with the given html template.

        Args:
            node: The possible pre node of a code block.
        '''
        children = list(node)
        if (len(children) == 1 and children[0].tag == 'code'):
            content = children[0].text.strip()
            language = children[0].attrib.get('class', content)
            language_in_content = 'class' not in children[0].attrib.keys()

            match = self.pattern.search(language)
            if match is not None:
                options = list(filter(None, match.group('options').split(':')))
                if language_in_content:
                    content = content[match.end():]

                content_blocks = list(filter(None, content.split('\n\n')))
                if 'random' in options:
                    shuffle(content_blocks)
                if 'split' not in options:
                    content_blocks = [reduce(lambda x, y: '\n\n'.join([x, y]), content_blocks)]

                images = []
                for block in content_blocks:
                    content_hash = ScratchTreeprocessor.hash_content(block)
                    self.update_required_images(content_hash, block)
                    images.append(content_hash)

                html_string = self.template.render({'images': images})
                parser = HtmlParser()
                new_node = parser.feed(html_string).close().get_root()

                node.tag = 'remove'
                node.text = ''
                node.append(new_node)
                node.remove(children[0])

    @staticmethod
    def hash_content(text):
        '''Finds the hash of the given text for image retrieval.

        Args:
            text: The text to hash.
        Returns:
            The hash of the text for image retrieval.
        '''
        return sha256(text.encode('utf8')).hexdigest()

    def update_required_images(self, content_hash, text):
        '''Adds the scratch code and hash to the verto result.

        Args:
            content_hash: The image hash.
            text: The source text of the image.
        '''
        self.scratch_images.add(ScratchImageMetaData(hash=content_hash, text=text))
