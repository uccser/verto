from markdown.extensions import Extension
from processors.panel import *
from processors.whitespace import *


class CSFGExtension(Extension):
   def extendMarkdown(self, md, md_globals):
       md.preprocessors.add('whitespace', WhitespacePreprocessor(md), '_begin')
       md.preprocessors.add('panelpre', PanelPreprocessor(md), '_begin')
       md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), "_begin")
