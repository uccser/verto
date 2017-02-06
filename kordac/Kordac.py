import markdown
import mdx_math
from kordac.KordacExtension import KordacExtension

class Kordac(object):
    """A converter object for converting markdown
    to HTML"""

    def run(self, markdown_string):
        kordac_extension = KordacExtension()
        kordac_extension.heading = None
        self.required_files = {}

        converter = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            mdx_math.MathExtension(enable_dollar_delimiter=True),
            kordac_extension])
        html = converter.convert(markdown_string)

        result = KordacResult(
            html=html,
            heading=kordac_extension.page_heading
        )
        return result


class KordacResult(object):
    """Object created by Kordac containing result of
    a conversion by run
    """

    def __init__(self, html=None, heading=None):
        self.html = html
        self.heading = heading
