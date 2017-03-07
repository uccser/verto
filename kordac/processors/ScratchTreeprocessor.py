from markdown.treeprocessors import Treeprocessor
from kordac.processors.utils import blocks_to_string, parse_argument, etree
from kordac.processors.errors.TagNotMatchedError import TagNotMatchedError
from collections import namedtuple
from hashlib import sha256
import re

class ScratchImageMetaData(namedtuple('ScratchImageMetaData', 'hash, text')):
    ''' Represents data required to make a scratch image.

    Keyword arguments:
        hash: hash of the scratch data
        text: text of the scratch code
    '''

class ScratchTreeprocessor(Treeprocessor):
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
        self.template = ext.jinja_templates[self.processor]
        self.scratch_images = ext.required_files['scratch_images']
        self.fenced_compatibility = 'fenced_code_block' in ext.compatibility

    def run(self, root):
        ''' Processes the html tree finding code tags where scratch
        code is used and replaces with template html.

        Args:
            root: The root of the document element tree.
        '''
        for node in root.iter('pre'):
            children = list(node)
            content = children[0].text.strip()
            compatibility_check = self.fenced_compatibility and (
                'class' in children[0].attrib.keys()
                and children[0].attrib['class'] == 'scratch'
            )
            print(compatibility_check)
            if (len(children) == 1 and children[0].tag == 'code'
             and (content.startswith('scratch\n') or compatibility_check)):
                content = content[len('scratch\n'):]
                content_hash = ScratchTreeprocessor.hash_content(content)
                self.update_required_images(content_hash, content)
                html_string = self.template.render({ 'hash': content_hash })
                new_node = etree.fromstring(html_string)

                node.tag = "remove"
                node.text = ""
                node.append(new_node)
                node.remove(children[0])

        # else:  # For compatibility with fenced_code extension
        #     print("START")
        #     root_string = etree.tostring(root, encoding="unicode", method="html")
        #     print(root_string)
        #     print("END")
        #
        #     for node in root.iter('pre'):
        #         children = list(node)
        #         content = children[0].text.strip()
        #         if len(children) == 1 and content.startswith('scratch\n'):
        #             content = content[len('scratch\n'):]
        #             content_hash = ScratchTreeprocessor.hash_content(content)
        #             self.update_required_images(content_hash, content)
        #             html_string = self.template.render({ 'hash': content_hash })
        #             new_node = etree.fromstring(html_string)
        #
        #             node.tag = "remove"
        #             node.text = ""
        #             node.append(new_node)
        #             node.remove(children[0])
            # elif (self.fenced_compatibility and len(children) == 1 and children[0].tag == 'code'
            # and 'class' in children[0].attrib and children[0].attrib['class'] == 'scratch'):
            #     content_hash = ScratchTreeprocessor.hash_content(content)
            #     self.update_required_images(content_hash, content)
            #     html_string = self.template.render({ 'hash': content_hash })
            #     node = etree.fromstring(html_string)
            #
            #     node.tag = "remove"
            #     node.text = ""
            #     node.append(node)

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
        '''Adds the scratch code and hash to the kordac result.

        Args:
            content_hash: The image hash.
            text: The source text of the image.
        '''
        self.scratch_images.add(ScratchImageMetaData(hash=content_hash, text=text))
