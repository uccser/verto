from markdown.inlinepatterns import Pattern
from kordac.processors.utils import *
from markdown.util import etree
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
        template_name = self.processor.get('template_name', self.processor)
        self.template = ext.jinja_templates[ext.processor_info[template_name]

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

        term = arugment_values['term']
        reference = arugment_values['reference-text']

        context = {
            'term': term,
            'text': text
        }

        if reference is not None:
            identifier = self.unique_slugify('glossary-' + term)
            self.ext_glossary_terms[term].append((reference, identifier))
            context['id'] = identifier

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)

        return node
