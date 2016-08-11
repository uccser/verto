from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
import bs4

class ScriptTreeProcessor(Treeprocessor):
    def __init__(self, scripts, *args, **kwargs):
        self.scripts = scripts
        super().__init__(*args, **kwargs)

    def run(self, root):
        for script in self.scripts:
            try:
                node = etree.fromstring(script)
            except:
                reformed = bs4.BeautifulSoup(script, 'html5lib').prettify()
                node = etree.fromstring(reformed)
            root.append(node)

        # for script in self.blockProcessor.scripts:
            # root.append(etree.fromstring(script))
