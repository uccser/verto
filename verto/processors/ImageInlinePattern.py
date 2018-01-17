from verto.utils.HtmlParser import HtmlParser
from verto.processors.utils import parse_arguments
from verto.utils.image_file_name_components import image_file_name_components
from markdown.inlinepatterns import Pattern
import re


class ImageInlinePattern(Pattern):
    '''Return a link element from the given match.'''

    def __init__(self, ext, *args, **kwargs):
        '''Create a inline image pattern.

        Args:
            ext: An instance of the Markdown class.
        '''
        self.processor = 'image-inline'
        self.arguments = ext.processor_info[self.processor]['arguments']
        self.pattern = ext.processor_info[self.processor]['pattern']
        self.compiled_re = re.compile('^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE)
        template_name = ext.processor_info.get('template_name', self.processor)
        self.template = ext.jinja_templates[template_name]
        self.relative_image_template = ext.jinja_templates['relative-file-link']
        self.required = ext.required_files['images']

    def handleMatch(self, match):
        ''' Inherited from Pattern. Accepts a match and returns an
        ElementTree element of a internal link.

        Args:
            match: The string of text where the match was found.
        Returns:
            An element tree node to be appended to the html tree.
        '''
        arguments = match.group('args')
        argument_values = parse_arguments(self.processor, arguments, self.arguments)

        context = dict()
        # check if internal or external image
        file_path = argument_values['file-path']
        external_path_match = re.search(r'^http', file_path)
        if external_path_match is None:  # internal image
            self.required.add(file_path)
            file_relative = True
            context.update(image_file_name_components(file_path))
        else:
            file_relative = False
        context['full_file_path'] = file_path
        context['file_relative'] = file_relative
        context['alt'] = argument_values.get('alt', None)
        context['caption'] = argument_values.get('caption', None)
        context['caption_link'] = argument_values.get('caption-link', None)
        context['source_link'] = argument_values.get('source', None)
        context['hover_text'] = argument_values.get('hover-text', None)

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        return parser.get_root()
