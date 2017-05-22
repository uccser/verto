from verto.processors.GenericTagBlockProcessor import GenericTagBlockProcessor
from verto.processors.utils import parse_arguments
from verto.utils.HtmlParser import HtmlParser
import re


class ImageBlockProcessor(GenericTagBlockProcessor):
    ''' Searches a Document for image tags e.g. {image file-path="<condition>"}
    adding any internal images to the verto extension final result.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will
                reside in.
        '''
        super().__init__('image', ext, *args, **kwargs)
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

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
        ''' Processes the block matching the image pattern, adding
        any internal images to the VertoExtension result.

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

        # check if internal or external image
        file_path = argument_values['file-path']
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_path = self.relative_image_template.render({'file_path': file_path})

        context = dict()
        context['file_path'] = file_path
        context['alt'] = argument_values.get('alt', None)
        context['caption'] = argument_values.get('caption', None)
        context['caption_link'] = argument_values.get('caption-link', None)
        context['source_link'] = argument_values.get('source', None)
        context['alignment'] = argument_values.get('alignment', None)
        context['hover_text'] = argument_values.get('hover-text', None)

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())
