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
from kordac.processors.TableOfContentsBlockProcessor import TableOfContentsBlockProcessor
from kordac.processors.ScratchTreeprocessor import ScratchTreeprocessor
from kordac.processors.ScratchCompatibilityPreprocessor import ScratchCompatibilityPreprocessor

from kordac.utils.UniqueSlugify import UniqueSlugify
from kordac.utils.HeadingNode import HeadingNode

from collections import defaultdict
from os import listdir
import os.path
import re
import json

from jinja2 import Environment, PackageLoader, select_autoescape

class KordacExtension(Extension):
    def __init__(self, processors=[], html_templates={}, extensions=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_files = defaultdict(set)
        self.title = None
        self.jinja_templates = self.loadJinjaTemplates(html_templates)
        self.processor_info = self.loadProcessorInfo()
        self.processors = processors
        self.custom_slugify = UniqueSlugify()
        self.glossary_terms = defaultdict(list)
        self.heading_tree = None

        self.compatibility = []
        for extension in extensions:
            if isinstance(extension, utils.string_type):
                if extension.endswith('codehilite'):
                    self.compatibility.append('hilite')
                if extension.endswith('fenced_code'):
                    self.compatibility.append('fenced_code_block')

    def extendMarkdown(self, md, md_globals):
        preprocessors = [
            ['comment', CommentPreprocessor(self, md), '_begin'],
            ['save-title', SaveTitlePreprocessor(self, md), '_end'],
            ['remove-title', RemoveTitlePreprocessor(self, md), '_end'],
        ]
        blockprocessors = [
        # Markdown overrides
            ['heading', HeadingBlockProcessor(self, md.parser), '<hashheader'],
        # Single line (in increasing complexity)
            ['table-of-contents', TableOfContentsBlockProcessor(self, md.parser), '_begin'],
            ['iframe', FrameBlockProcessor(self, md.parser), '_begin'],
            ['interactive', InteractiveBlockProcessor(self, md.parser), '_begin'],
            ['button-link', ButtonLinkBlockProcessor(self, md.parser), '_begin'],
            ['image', ImageBlockProcessor(self, md.parser), '_begin'],
            ['video', VideoBlockProcessor(self, md.parser), '_begin'],
            ['conditional', ConditionalProcessor(self, md.parser), '_begin'],
        # Multiline
            ['boxed-text', BoxedTextBlockProcessor(self, md.parser), '_begin'],
            ['panel', PanelBlockProcessor(self, md.parser), '_begin'],
        ]
        inlinepatterns = [ # A special treeprocessor
            ['relative-link', RelativeLinkPattern(self, md), '_begin'],
            ['glossary-link', GlossaryLinkPattern(self, md), '_begin'],
        ]
        treeprocessors = [
            ['scratch', ScratchTreeprocessor(self, md), '>inline' if 'hilite' not in self.compatibility else '<hilite'],
        ]
        postprocessors = []

        for processor_data in preprocessors:
            if processor_data[0] in self.processors:
                md.preprocessors.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in blockprocessors:
            if processor_data[0] in self.processors:
                md.parser.blockprocessors.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in inlinepatterns:
            if processor_data[0] in self.processors:
                md.inlinePatterns.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in treeprocessors:
            if processor_data[0] in self.processors:
                md.treeprocessors.add(processor_data[0], processor_data[1], processor_data[2])
        for processor_data in postprocessors:
            if processor_data[0] in self.processors:
                md.postprocessors.add(processor_data[0], processor_data[1], processor_data[2])

        md.postprocessors.add('remove', RemovePostprocessor(md), '_end')
        md.postprocessors.add('beautify', BeautifyPostprocessor(md), '_end')
        md.postprocessors.add('jinja', JinjaPostprocessor(md), '_end')

        # Compatibility modules
        if 'hilite' in self.compatibility and 'fenced_code_block' in self.compatibility and 'scratch' in self.processors:
            md.preprocessors.add('scratch-compatibility', ScratchCompatibilityPreprocessor(self, md), '<fenced_code_block')

    def clear_saved_data(self):
        self.title = None
        self.custom_slugify.clear()
        self.heading_tree = None
        for key in self.required_files.keys():
            self.required_files[key].clear()

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
