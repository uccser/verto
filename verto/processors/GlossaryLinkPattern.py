from markdown.inlinepatterns import Pattern
from verto.processors.utils import parse_arguments
from verto.utils.HtmlParser import HtmlParser
import re


class GlossaryLinkPattern(Pattern):
    '''Return a glossary link element from the given match

    Matches:
        {glossary-link term="super-serious-term"}Super Serious Term{glossary-link end}
    Returns:
        <p>
         <a class="glossary-term" data-glossary-term="super-serious-term">
          Super Serious Term
         </a>
        </p>
    '''

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext = ext
        self.processor = 'glossary-link'
        self.pattern = self.ext.processor_info['glossary-link']['pattern']
        self.compiled_re = re.compile(r'^(.*?){}(.*)$'.format(self.pattern), re.DOTALL | re.UNICODE)
        self.arguments = ext.processor_info[self.processor]['arguments']
        template_name = ext.processor_info.get('template_name', self.processor)
        self.template = ext.jinja_templates[template_name]

        self.ext_glossary_terms = ext.glossary_terms
        self.unique_slugify = ext.custom_slugify

    def handleMatch(self, match):
        '''
        Turns a match into a glossary-link and adds the slug and
        identifier to the extension as part of the final result.
        Args:
            match: The string of text where the match was found.
        Returns:
            An element tree node to be appended to the html tree.
        '''
        text = match.group('text')
        arguments = match.group('args')
        argument_values = parse_arguments(self.processor, arguments, self.arguments)

        term = argument_values['term']
        reference = argument_values.get('reference-text', None)

        context = {
            'term': term,
            'text': text
        }

        glossary_reference = self.ext_glossary_terms[term]
        if reference is not None:
            identifier = self.unique_slugify('glossary-' + term)
            glossary_reference.append((reference, identifier))
            context['id'] = identifier

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        return parser.get_root()
