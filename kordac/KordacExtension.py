from markdown.extensions import Extension
import markdown.util as utils

from kordac.processors.PanelBlockProcessor import PanelBlockProcessor
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.processors.ImageBlockProcessor import ImageBlockProcessor
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from kordac.processors.RelativeLinkPattern import RelativeLinkPattern
from kordac.processors.NumberedHashHeaderProcessor import NumberedHashHeaderProcessor
from kordac.processors.RemoveTitlePreprocessor import RemoveTitlePreprocessor
from kordac.processors.SaveTitlePreprocessor import SaveTitlePreprocessor
from kordac.processors.DjangoPostProcessor import DjangoPostProcessor
from kordac.processors.GlossaryLinkBlockProcessor import GlossaryLinkBlockProcessor
from kordac.processors.ButtonLinkBlockProcessor import ButtonLinkBlockProcessor
from kordac.processors.BoxedTextBlockProcessor import BoxedTextBlockProcessor
from kordac.processors.BeautifyPostprocessor import BeautifyPostprocessor

from collections import defaultdict
from os import listdir
import os.path
import re
import json

from jinja2 import Environment, PackageLoader, select_autoescape

class KordacExtension(Extension):
    def __init__(self, processors=[], html_templates={}, *args, **kwargs):
        self.page_scripts = []
        self.required_files = defaultdict(set)
        self.title = None
        self.html_templates = self.loadHTMLTemplates(html_templates)
        self.jinja_templates = self.loadJinjaTemplates(html_templates)
        self.processor_info = self.loadProcessorInfo()
        self.processors = processors
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        preprocessors = [
            ['save-title', SaveTitlePreprocessor(self, md), '_end'],
            ['remove-title', RemoveTitlePreprocessor(self, md), '_end'],
            ['comment', CommentPreprocessor(self, md), '_begin'],
        ]
        inlinepatterns = [
            ['relative-link', RelativeLinkPattern(self, md), '_begin']
        ]
        blockprocessors = [
            #['hashheader', NumberedHashHeaderProcessor(self, md.parser), '_begin'],
            ['panel', PanelBlockProcessor(self, md.parser), '>ulist'],
            #['glossary-link', GlossaryLinkBlockProcessor(self, md.parser), '_begin'],
            #['interactive', InteractiveBlockProcessor(self, md.parser), '_begin'],
            #['video', VideoBlockProcessor(self, md.parser), '_begin'],
            ['image', ImageBlockProcessor(self, md.parser), '_begin'],
            ['button-link', ButtonLinkBlockProcessor(self, md.parser), '_begin'],
            ['boxed-text', BoxedTextBlockProcessor(self, md.parser), '_begin']
        ]

        for processor_data in preprocessors:
            if processor_data[0] in self.processors:
                md.preprocessors.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in inlinepatterns:
            if processor_data[0] in self.processors:
                md.inlinePatterns.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in blockprocessors:
            if processor_data[0] in self.processors:
                md.parser.blockprocessors.add(processor_data[0], processor_data[1], processor_data[2])

        md.postprocessors.add('beautify', BeautifyPostprocessor(md), '_end')

    def clear_saved_data(self):
        self.title = None
        self.page_scripts = []
        self.required_files.clear()

    def loadHTMLTemplates(self, custom_templates):
        templates = {}
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')):
            processor_name = re.search(r'(.*?).html', file).groups()[0]
            if processor_name in custom_templates:
                templates[processor_name] = custom_templates[processor_name]
            else:
                templates[processor_name] = open(os.path.join(os.path.dirname(__file__), 'html-templates', file)).read()
        return templates

    def loadJinjaTemplates(self, custom_templates):
        templates = {}
        env = Environment(
                loader=PackageLoader('kordac', 'html-templates'),
                autoescape=select_autoescape(['html'])
                )
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')):
            processor_name = re.search(r'(.*?).html', file).groups()[0]
            if processor_name in custom_templates:
                templates[processor_name] = env.from_string(custom_templates[processor_name])
            else:
                templates[processor_name] = env.get_template(file)
        return templates

    def loadProcessorInfo(self):
        json_data = open(os.path.join(os.path.dirname(__file__), 'processor-info.json')).read()
        return json.loads(json_data)
