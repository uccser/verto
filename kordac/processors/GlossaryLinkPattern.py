from kordac.processors.utils import check_required_parameters, parse_argument
from markdown.util import etree
import markdown.inlinepatterns
import re


class GlossaryLinkPattern(markdown.inlinepatterns.Pattern):
    """Return a glossary link element from the given match

    Matches:
        {glossary-link term="super-serious-term"}Super Serious Term{glossary-link end}
    Returns:
        <p>
         <a class="glossary-term" data-glossary-term="super-serious-term">
          Super Serious Term
         </a>
        </p>
    """

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.processor = 'glossary-link'
        self.pattern = self.ext.processor_info['glossary-link']['pattern']
        self.compiled_re = re.compile('^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE) # TODO raw string prefix
        self.template = self.ext.jinja_templates[self.processor]
        self.required_parameters = self.ext.processor_info[self.processor]['required_parameters']
        self.optional_parameters = self.ext.processor_info[self.processor]['optional_parameter_dependencies']

    def handleMatch(self, match):

        text = match.group('text')
        arguments = match.group('args')

        term = parse_argument('term', arguments)
        reference = parse_argument('reference-text', arguments)

        context = dict()
        context['term'] = term
        context['text'] = text

        identifier = 'glossary-{}{}'

        if reference is not None:
            if term in self.ext.glossary_term_occurance_counter.keys():
                self.ext.glossary_term_occurance_counter[term] += 1
            else:
                self.ext.glossary_term_occurance_counter[term] = 1

            count = self.ext.glossary_term_occurance_counter[term]
            if count > 1:
                identifier = identifier.format(term, '-' + str(count))
            else:
                identifier = identifier.format(term, '')

            context['id'] = identifier

        check_required_parameters(self.processor, self.required_parameters, context)

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)

        return node

