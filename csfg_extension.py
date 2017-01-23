from markdown.extensions import Extension

from processors.panel import *
from processors.comment import *
from processors.video import *
from processors.image import *
from processors.interactive import *
from processors.heading import *
from processors.django import *
from processors.glossary import *

from collections import defaultdict
from os import listdir
import re

class CSFGExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.page_scripts = []
        self.required_files = defaultdict(set)
        self.page_heading = None
        self.html_templates = {}
        super().__init__(*args, **kwargs)

    # md = instance of Markdown class we are modifying
    def extendMarkdown(self, md, md_globals):
        print(self)

        self.loadHTMLTemplates()
        print(self.html_templates)
        # print(md.parser)
        # print('hello, you\'ve called extendMarkdown')
        # NTS not quite in right order with existing md tags
        # TODO compare to regex list in existing CSFG Generator for order
        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), ">ulist")
        md.parser.blockprocessors.add('glossary-link', GlossaryLinkBlockProcessor(self, md.parser), "_begin")
        md.parser.blockprocessors.add('interactive', InteractiveBlockProcessor(self, md.parser), "_begin")
        md.parser.blockprocessors.add('video', VideoBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('image', ImageBlockProcessor(self, md.parser), "_begin")

        md.parser.blockprocessors['hashheader'] = NumberedHashHeaderProcessor(self, md.parser) # format of this one doesn't match the others?
        # NTS test this
        # md.parser.blockprocessors.add('hashheader', NumberedHashHeaderProcessor(md.parser), "_begin")

        md.parser.blockprocessors.add('comment', CommentBlockProcessor(md.parser), "_begin")
        md.preprocessors.add('commentpre', CommentPreprocessor(md), '_begin')

        # NTS have not looked into what this does
        # md.postprocessors.add('interactivepost', DjangoPostProcessor(self, md.parser), '_end')

        # print(md.parser.blockprocessors)
        # for i in md.parser.blockprocessors:
            # print(i)


    def reset(self):
        self.page_scripts = []
        self.required_files = {}


    def loadHTMLTemplates(self):
        for file in listdir('html-templates'): # TODO there has got to be a better way to do this
            if 'swp' not in file: # HACK have vim files open atm, so they are getting in the way...
                tag_name = re.search(r'(.*?).html', file).groups()[0]
                self.html_templates[tag_name] = open('html-templates/' + file).read()



