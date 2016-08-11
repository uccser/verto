from markdown.extensions import Extension
from processors.panel import *
from processors.comment import *
from processors.video import *
from processors.image import *
from processors.interactive import *
from processors.scripts import *

page_scripts = [
    "<script type='text/javascript' src='js/third-party/jquery.js'></script>",
    "<script type='text/javascript' src='js/third-party/materialize.min.js'></script>",
    "<script type='text/javascript' src='js/third-party/featherlight.min.js'></script>",
    "<script type='text/javascript' src='js/website.js'></script>",
    """<script type="text/x-mathjax-config">MathJax.Hub.Config({"HTML-CSS": { linebreaks: { automatic: true } },});</script>""",
    """<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>""",
    "<script src='js/third-party/modernizr.js'></script>"
]

class CSFGExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        self.imageprocessor = ImageBlockProcessor(md.parser)
        self.interactiveBlockProcessor = InteractiveBlockProcessor(md.parser)
        self.interactiveTreeProcessor = InteractiveTreeProcessor(self.interactiveBlockProcessor, md.parser)

        md.parser.blockprocessors.add('panel', PanelBlockProcessor(md.parser), ">ulist")
        md.parser.blockprocessors.add('interactive', self.interactiveBlockProcessor, "_begin")
        md.treeprocessors.add('interactiveTree', self.interactiveTreeProcessor, "_begin")
        md.treeprocessors.add('scriptTree', ScriptTreeProcessor(page_scripts, md.parser), "<interactiveTree")
        md.parser.blockprocessors.add('video', VideoBlockProcessor(md.parser), "_begin")
        md.parser.blockprocessors.add('image', self.imageprocessor, "_begin")
        md.parser.blockprocessors.add('comment', CommentBlockProcessor(md.parser), "_begin")
        md.preprocessors.add('commentpre', CommentPreprocessor(md), '_begin')
