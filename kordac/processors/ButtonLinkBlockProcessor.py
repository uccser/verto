from markdown.blockprocessors import BlockProcessor
from kordac.processors.utils import parse_argument, check_argument_requirements
import re
from markdown.util import etree

class ButtonLinkBlockProcessor(BlockProcessor):
    '''Searches blocks provided by markdown and turns button-link tags e.g. {button-link link="www.example.com" text="Lipsum" file="no"} and replaces them with the html template from the html-template directory.
    '''
    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'button-link'
        self.template = ext.jinja_templates[self.processor]
        self.relative_file_template = ext.jinja_templates['relative-file-link']
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def test(self, parent, block):
        '''Return whether the provided document contains comments needing removal.

        Args:
            block: A string to test against.

        Returns:
            True if the document needs to be processed.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Inherited from BlockProcessor class from Markdown.

        Args:
            parent: Element (from ElementTree library) which this block resides within. The created html-template elements are placed within here.
            blocks: Blocks of text where the first block matched via the test method.
        '''
        block = blocks.pop(0)
        match = self.pattern.search(block)

        arguments = match.group('args')
        check_argument_requirements(self.processor, arguments, self.required_parameters, self.optional_parameters)

        context = dict()
        context['link'] = parse_argument('link', arguments)
        context['text'] = parse_argument('text', arguments)
        context['file'] = parse_argument('file', arguments, 'no').lower() == 'yes'

        if context['file']:
            context['link'] = self.relative_file_template.render({'file_path': context['link']})

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)
