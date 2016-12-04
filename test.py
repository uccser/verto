from markdown.extensions import Extension

from processors.glossary import *
from processors.panel import *

from collections import defaultdict


class CSFGExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.page_scripts = []
        self.required_files = defaultdict(set)
        self.page_heading = None
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        # same as blpr['glossary'] = GLBP(md.parser)
        md.parser.blockprocessors.add('glossary', GlossaryLinkBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), ">ulist")


    def reset(self):
        self.page_scripts = []
        self.required_files = {}

