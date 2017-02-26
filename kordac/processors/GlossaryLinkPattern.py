from kordac.processors.utils import check_required_parameters, parse_argument
import markdown.util as util
import markdown.inlinepatterns
import re


class GlossaryLinkPattern(markdown.inlinepatterns.Pattern):
    # occurance_counter = {}

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'glossary-link'
        self.pattern = ext.processor_info['glossary-link']['pattern']
        self.compiled_re = re.compile('^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE) # TODO raw string prefix
        self.template = ext.jinja_templates[self.processor]
        self.required_parameters = ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = ext.processor_info[self.processor]['optional_parameter_dependencies']

    def handleMatch(self, match):

        text = match.group('text')
        arguments = match.group('args')

        term = parse_argument('term', arguments)
        identifier = parse_argument('id', arguments)

        context = dict()
        context['term'] = term
        context['id'] = identifier
        context['text'] = text

        check_required_parameters(self.processor, self.required_parameters, context)

        html_string = self.template.render(context)
        node = util.etree.fromstring(html_string)

        return node

