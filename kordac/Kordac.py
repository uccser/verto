import markdown
import mdx_math
from kordac.KordacExtension import KordacExtension

class Kordac():

    def run(self, md_string):
        self.heading = 'I am a heading'
        self.required_files = {}
        self.html_string = ''
        ext = KordacExtension()
        converter = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            mdx_math.MathExtension(enable_dollar_delimiter=True),
            ext])

        self.html_string = converter.convert(md_string)
        self.heading = ext.page_heading

        return self
