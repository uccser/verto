from markdown.extensions import Extension

from processors.panel import *
from processors.comment import *
from processors.video import *
from processors.image import *
from processors.interactive import *
from processors.heading import *
from processors.django import *

class CSFGExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.page_scripts = []
        self.required_files = {}
        self.page_heading = None
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        # self.imageprocessor = ImageBlockProcessor(md.parser)
        # pagescripts = []
        # self.interactiveBlockProcessor = InteractiveBlockProcessor(pagescripts, md.parser)
        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), ">ulist")
        md.parser.blockprocessors['hashheader'] = NumberedHashHeaderProcessor(self, md.parser)
        md.parser.blockprocessors.add('interactive', InteractiveBlockProcessor(self, md.parser), "_begin")
        md.parser.blockprocessors.add('video', VideoBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('image', ImageBlockProcessor(self, md.parser), "_begin")
        md.parser.blockprocessors.add('comment', CommentBlockProcessor(md.parser), "_begin")
        md.preprocessors.add('commentpre', CommentPreprocessor(md), '_begin')
        md.postprocessors.add('interactivepost', DjangoPostProcessor(self, md.parser), '_end')

    def reset(self):
        self.page_scripts = []
        self.required_files = {}
