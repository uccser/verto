from markdown.extensions import Extension

from kordac.processors.PanelBlockProcessor import PanelBlockProcessor
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from kordac.processors.CommentBlockProcessor import CommentBlockProcessor
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.processors.ImageBlockProcessor import ImageBlockProcessor
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from kordac.processors.NumberedHashHeaderProcessor import NumberedHashHeaderProcessor
from kordac.processors.HeadingPreprocessor import HeadingPreprocessor
from kordac.processors.DjangoPostProcessor import DjangoPostProcessor
from kordac.processors.GlossaryLinkBlockProcessor import GlossaryLinkBlockProcessor
from kordac.processors.ButtonPreprocessor import ButtonPreprocessor

from collections import defaultdict
from os import listdir
import os.path
import re
import json

class KordacExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.page_scripts = []
        self.required_files = defaultdict(set)
        self.page_heading = None
        self.html_templates = {}
        self.tag_patterns = {}
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):

        self.loadHTMLTemplates()
        self.loadTagPatterns()

        md.preprocessors.add('headingpre', HeadingPreprocessor(self, md), '_begin')
        md.parser.blockprocessors.add('panel', PanelBlockProcessor(self, md.parser), ">ulist")
        # md.parser.blockprocessors.add('glossary-link', GlossaryLinkBlockProcessor(self, md.parser), "_begin")
        # md.parser.blockprocessors.add('interactive', InteractiveBlockProcessor(self, md.parser), "_begin")
        # md.parser.blockprocessors.add('video', VideoBlockProcessor(self, md.parser), "_begin")
        # md.parser.blockprocessors.add('image', ImageBlockProcessor(self, md.parser), "_begin")

        md.parser.blockprocessors.add('hashheader', NumberedHashHeaderProcessor(self, md.parser), "_begin")

        # md.parser.blockprocessors.add('comment', CommentBlockProcessor(self, md.parser), "_begin")
        # md.preprocessors.add('commentpre', CommentPreprocessor(self, md), '_begin')
        # md.preprocessors.add('button', ButtonPreprocessor(self, md), '_begin')

        # NTS have not looked into what this does
        # md.postprocessors.add('interactivepost', DjangoPostProcessor(self, md.parser), '_end')


    def reset(self):
        self.page_scripts = []
        self.required_files = {}


    def loadHTMLTemplates(self):
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')): # TODO there has got to be a better way to do this
            if 'swp' not in file: # HACK have vim files open atm, so they are getting in the way...
                tag_name = re.search(r'(.*?).html', file).groups()[0]
                self.html_templates[tag_name] = open(os.path.join(os.path.dirname(__file__), 'html-templates', file)).read()

    def loadTagPatterns(self):
        pattern_data = open(os.path.join(os.path.dirname(__file__), 'regex-list.json')).read()
        self.tag_patterns = json.loads(pattern_data)
