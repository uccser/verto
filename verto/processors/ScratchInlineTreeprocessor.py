from verto.processors.ScratchTreeprocessor import ScratchTreeprocessor
from verto.utils.HtmlParser import HtmlParser
import re


class ScratchInlineTreeprocessor(ScratchTreeprocessor):
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
        super().__init__(ext, *args, **kwargs)
        self.processor = 'scratch-inline'
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.scratch_images = ext.required_files['scratch_images']
        self.fenced_compatibility = 'fenced_code_block' in ext.compatibility

    def run(self, root):
        ''' Processes the html tree finding code tags outside pre tags
        where scratch code is used and replaces with template html.

        Args:
            root: The root of the document element tree.
        '''
        code_elements = set()
        pre_code_elements = set()
        for node in root.iterfind('.//code'):
            code_elements.add(node)
        for node in root.iterfind('.//pre/code'):
            pre_code_elements.add(node)

        for node in (code_elements - pre_code_elements):
            self.process_html(node)

    def process_html(self, node):
        ''' Checks if given node is a scratch code tag and replaces
        with the given html template.

        Args:
            node: The possible pre node of a code block.
        '''
        content = node.text.strip()
        match = self.pattern.match(content)

        if match is not None:
            block = content[match.end():]
            content_hash = self.hash_content(block)
            self.update_required_images(content_hash, block)

            parser = HtmlParser()
            html_string = self.template.render({'hash': content_hash})
            new_node = parser.feed(html_string).close().get_root()

            node.tag = 'remove'
            node.text = ''
            node.append(new_node)
