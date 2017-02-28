
from kordac.processors.utils import check_required_parameters
from markdown.util import etree
import markdown.util as util
import markdown.inlinepatterns
import re

class RelativeLinkPattern(markdown.inlinepatterns.Pattern):
    """Return a link element from the given match.

    Only matches:
        - Markdown links using []() syntax.
        - Links that don't start with:
            - http:
            - https:
            - ftp:
            - ftps:
            - mailto:
            - news:
    """

    def __init__(self, ext, *args, **kwargs):
        self.processor = 'relative-link'
        self.pattern = ext.processor_info[self.processor]['pattern']
        self.compiled_re = re.compile('^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE)
        self.template = ext.jinja_templates[self.processor]

    def handleMatch(self, match):

        context = dict()
        context['link_path'] = match.group('link_url')
        context['text'] = match.group('link_text')

        check_required_parameters(self.processor, self.required_parameters, context)

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)

        return node

