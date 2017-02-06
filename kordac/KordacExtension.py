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
import yaml


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

        processors = {
            'preprocessors': {
                'heading': ['headingpre', HeadingPreprocessor(self, md), '_begin'],
                'comment': ['commentpre', CommentPreprocessor(self, md), '_begin'],
                'button': ['button', ButtonPreprocessor(self, md), '_begin']
                },
            'blockprocessors': {
                'heading': ['hashheader', NumberedHashHeaderProcessor(self, md.parser), '_begin'],
                'panel': ['panel', PanelBlockProcessor(self, md.parser), '>ulist'],
                'glossary-link': ['glossary-link', GlossaryLinkBlockProcessor(self, md.parser), '_begin'],
                'interactive': ['interactive', InteractiveBlockProcessor(self, md.parser), '_begin'],
                'video': ['video', VideoBlockProcessor(self, md.parser), '_begin'],
                'image': ['image', ImageBlockProcessor(self, md.parser), '_begin'],
                'comment': ['comment', CommentBlockProcessor(self, md.parser), '_begin']
                },
            }


        with open('kordac/tags.yaml', 'r') as f:
            tags = yaml.load(f)
            tag_processor = None
            for tag in tags['enabled-tags']:
                if tag in processors['preprocessors']:
                    tag_processor = processors['preprocessors'].get(tag)
                    md.preprocessors.add(tag_processor[0], tag_processor[1], tag_processor[2])
                if tag in processors['blockprocessors']:
                    tag_processor = processors['blockprocessors'].get(tag)
                    md.parser.blockprocessors.add(tag_processor[0], tag_processor[1], tag_processor[2])


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
