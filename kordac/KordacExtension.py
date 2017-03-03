from markdown.extensions import Extension
import markdown.util as utils

from kordac.processors.PanelBlockProcessor import PanelBlockProcessor
from kordac.processors.CommentPreprocessor import CommentPreprocessor
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.processors.ImageBlockProcessor import ImageBlockProcessor
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from kordac.processors.RelativeLinkPattern import RelativeLinkPattern
from kordac.processors.RemoveTitlePreprocessor import RemoveTitlePreprocessor
from kordac.processors.SaveTitlePreprocessor import SaveTitlePreprocessor
from kordac.processors.GlossaryLinkPattern import GlossaryLinkPattern
from kordac.processors.ButtonLinkBlockProcessor import ButtonLinkBlockProcessor
from kordac.processors.BoxedTextBlockProcessor import BoxedTextBlockProcessor
from kordac.processors.BeautifyPostprocessor import BeautifyPostprocessor
from kordac.processors.ConditionalProcessor import ConditionalProcessor
from kordac.processors.RemovePostprocessor import RemovePostprocessor
from kordac.processors.JinjaPostprocessor import JinjaPostprocessor
from kordac.processors.HeadingBlockProcessor import HeadingBlockProcessor
from kordac.processors.FrameBlockProcessor import FrameBlockProcessor

from kordac.utils.UniqueSlugify import UniqueSlugify
from kordac.utils.HeadingNode import HeadingNode

from collections import defaultdict
from os import listdir
import os.path
import re
import json

from jinja2 import Environment, PackageLoader, select_autoescape

class KordacExtension(Extension):
    def __init__(self, processors=[], html_templates={}, *args, **kwargs):
        self.required_files = defaultdict(set)
        self.title = None
        self.jinja_templates = self.loadJinjaTemplates(html_templates)
        self.processor_info = self.loadProcessorInfo()
        self.processors = processors
        self.glossary_term_occurance_counter = {}
        self.custom_slugify = UniqueSlugify()
        self.heading_tree = None
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        preprocessors = [
            ['save-title', SaveTitlePreprocessor(self, md), '_end'],
            ['remove-title', RemoveTitlePreprocessor(self, md), '_end'],
            ['comment', CommentPreprocessor(self, md), '_begin'],
        ]
        inlinepatterns = [
            ['relative-link', RelativeLinkPattern(self, md), '_begin'],
            ['glossary-link', GlossaryLinkPattern(self, md), '_begin']
        ]
        blockprocessors = [
            ['panel', PanelBlockProcessor(self, md.parser), '>ulist'],
            ['interactive', InteractiveBlockProcessor(self, md.parser), '_begin'],
            ['video', VideoBlockProcessor(self, md.parser), '_begin'],
            ['conditional', ConditionalProcessor(self, md.parser), '_begin'],
            ['image', ImageBlockProcessor(self, md.parser), '_begin'],
            ['button-link', ButtonLinkBlockProcessor(self, md.parser), '_begin'],
            ['boxed-text', BoxedTextBlockProcessor(self, md.parser), '_begin'],
            ['heading', HeadingBlockProcessor(self, md.parser), '_begin'],
            ['iframe', FrameBlockProcessor(self, md.parser), '_begin']
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

        md.postprocessors.add('remove', RemovePostprocessor(md), '_end')
        md.postprocessors.add('beautify', BeautifyPostprocessor(md), '_end')
        md.postprocessors.add('jinja', JinjaPostprocessor(md), '_end')

    def clear_saved_data(self):
        self.title = None
        self.required_files.clear()
        self.custom_slugify.clear()
        self.heading_tree = None

    def loadJinjaTemplates(self, custom_templates):
        templates = {}
        env = Environment(
                loader=PackageLoader('kordac', 'html-templates'),
                autoescape=select_autoescape(['html'])
                )
        for file in listdir(os.path.join(os.path.dirname(__file__), 'html-templates')):
            html_file = re.search(r'(.*?).html$', file)
            if html_file:
                processor_name = html_file.groups()[0]
                if processor_name in custom_templates:
                    templates[processor_name] = env.from_string(custom_templates[processor_name])
                else:
                    templates[processor_name] = env.get_template(file)
        return templates

    def loadProcessorInfo(self):
        json_data = open(os.path.join(os.path.dirname(__file__), 'processor-info.json')).read()
        return json.loads(json_data)

    def get_heading_tree(self):
        return self.heading_tree

    def _set_heading_tree(self, tree):
        assert isinstance(tree, tuple)
        assert all(isinstance(child, HeadingNode) for child in tree)
        self.heading_tree = tree
