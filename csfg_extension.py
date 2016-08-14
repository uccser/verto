from markdown.extensions import Extension
from processors.panel import *
from processors.comment import *
from processors.video import *
from processors.image import *
from processors.interactive import *
from processors.heading import *

class CSFGExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        self.imageprocessor = ImageBlockProcessor(md.parser)
        self.interactiveBlockProcessor = InteractiveBlockProcessor(md.parser)

        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), ">ulist")
        md.parser.blockprocessors['hashheader'] = NumberedHashHeaderProcessor(md.parser)
        md.parser.blockprocessors.add('interactive', self.interactiveBlockProcessor, "_begin")
        md.parser.blockprocessors.add('video', VideoBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('image', self.imageprocessor, "_begin")
        md.parser.blockprocessors.add('comment', CommentBlockProcessor(md.parser), "_begin")
        md.preprocessors.add('commentpre', CommentPreprocessor(md), '_begin')
        md.postprocessors.add('interactivepost', InteractivePostProcessor(self.interactiveBlockProcessor, md), '_end')
