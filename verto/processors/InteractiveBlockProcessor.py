from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.processors.utils import parse_arguments
from verto.utils.HtmlParser import HtmlParser
import re


class InteractiveBlockProcessor(GenericTagBlockProcessor):
    '''Searches a Document for interactive tags:
        e.g. {interactive name='example' type='in-page'}
        These are then replaced with the html template.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: An instance of the Verto Extension.
        '''
        super().__init__('interactive', ext, *args, **kwargs)
        self.relative_file_template = ext.jinja_templates['relative-file-link']
        self.scripts = ext.required_files['page_scripts']
        self.required = ext.required_files['interactives']
        self.required_images = ext.required_files['images']

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            block: The block to be tested.
        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.match(block) is not None

    def run(self, parent, blocks):
        ''' Processes the block matching the heading and adding to the
        html tree and the verto heading tree.

        Args:
            parent: The parent node of the element tree that children
                will reside in.
            blocks: A list of strings of the document, where the
                first block tests true.
        '''
        block = blocks.pop(0)

        match = self.pattern.match(block)
        before = block[:match.start()]
        after = block[match.end():]

        if before.strip() != '':
            self.parser.parseChunk(parent, before)
        if after.strip() != '':
            blocks.insert(0, after)

        arguments = match.group('args')
        argument_values = parse_arguments(self.processor, arguments, self.arguments)

        name = argument_values['name']
        interactive_type = argument_values['type']
        text = argument_values.get('text', None)
        parameters = argument_values.get('parameters', None)

        # add to list of interactives
        self.required.add(name)

        if interactive_type == 'in-page':
            self.scripts.add('interactive/{}/scripts.html'.format(name))

        context = dict()
        context['type'] = interactive_type
        context['name'] = name
        context['text'] = text
        context['parameters'] = parameters

        if interactive_type == 'whole-page':
            file_path = argument_values.get('thumbnail', None)
            if file_path is None:
                file_path = '{}/thumbnail.png'.format(name)

            external_path_match = re.search(r'^http', file_path)
            if external_path_match is None:  # internal image
                self.required_images.add(file_path)
                file_path = self.relative_file_template.render({'file_path': file_path})
            context['file_path'] = file_path

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())
