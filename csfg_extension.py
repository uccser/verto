from markdown.extensions import Extension
from processors.panel import *
from processors.comment import *
from processors.video import *


class CSFGExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('video', VideoBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('comment', CommentBlockProcessor(md.parser), "_begin")
        md.preprocessors.add('commentpre', CommentPreprocessor(md), '_begin')
