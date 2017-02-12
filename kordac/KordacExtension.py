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
from kordac.processors.ButtonLinkBlockProcessor import ButtonLinkBlockProcessor

from collections import defaultdict
from os import listdir
import os.path
import re
import json

from jinja2 import Environment, PackageLoader, select_autoescape


class KordacExtension(Extension):
    def __init__(self, tags=[], html_templates={}, *args, **kwargs):
        self.page_scripts = []
        self.required_files = defaultdict(set)
        self.page_heading = None
        self.html_templates = self.loadHTMLTemplates(html_templates)
        self.jinja_templates = self.loadJinjaTemplates(html_templates)
        self.tag_patterns = self.loadTagPatterns()
        self.tags = tags
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        processors = {
            'preprocessors': {
                'headingpre': ['headingpre', HeadingPreprocessor(self, md), '_begin'],
                #'commentpre': ['commentpre', CommentPreprocessor(self, md), '_begin'],
                },
            'blockprocessors': {
                #'heading': ['hashheader', NumberedHashHeaderProcessor(self, md.parser), '_begin'],
                #'panel': ['panel', PanelBlockProcessor(self, md.parser), '>ulist'],
                #'glossary-link': ['glossary-link', GlossaryLinkBlockProcessor(self, md.parser), '_begin'],
                #'interactive': ['interactive', InteractiveBlockProcessor(self, md.parser), '_begin'],
                #'video': ['video', VideoBlockProcessor(self, md.parser), '_begin'],
                #'image': ['image', ImageBlockProcessor(self, md.parser), '_begin'],
                #'comment': ['comment', CommentBlockProcessor(self, md.parser), '>ulist'],
                #'button-link': ['button-link', ButtonLinkBlockProcessor(self, md.parser), '_begin']
                },
            }

        for tag in self.tags:
            if tag in processors['preprocessors']:
                tag_processor = processors['preprocessors'].get(tag)
                md.preprocessors.add(tag_processor[0], tag_processor[1], tag_processor[2])
            if tag in processors['blockprocessors']:
                tag_processor = processors['blockprocessors'].get(tag)
                md.parser.blockprocessors.add(tag_processor[0], tag_processor[1], tag_processor[2])

    def clear_saved_data(self):
        self.heading = None
        self.page_scripts = []
        self.required_files = {}

    def loadHTMLTemplates(self, custom_templates):
        templates = {}
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')):
            tag_name = re.search(r'(.*?).html', file).groups()[0]
            if tag_name in custom_templates:
                templates[tag_name] = custom_templates[tag_name]
            else:
                templates[tag_name] = open(os.path.join(os.path.dirname(__file__), 'html-templates', file)).read()
        return templates

    def loadJinjaTemplates(self, custom_templates):
        templates = {}
        env = Environment(
                loader=PackageLoader('kordac', 'html-templates'),
                autoescape=select_autoescape(['html'])
                )
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')):
            tag_name = re.search(r'(.*?).html', file).groups()[0]
            if tag_name in custom_templates:
                templates[tag_name] = custom_templates[tag_name]
            else:
                templates[tag_name] = env.get_template(file)
        return templates

    def loadTagPatterns(self):
        pattern_data = open(os.path.join(os.path.dirname(__file__), 'regex-list.json')).read()
        return json.loads(pattern_data)
