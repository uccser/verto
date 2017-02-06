import markdown
import mdx_math
from kordac.KordacExtension import KordacExtension

class Kordac(object):
    """A converter object for converting markdown
    with complex tags to HTML.
    """

    def run(self, text, tags, html_templates):
        """Return a KordacResult object after converting
        the given markdown string.

        Args:
            text: A string of Markdown text to be converted.

        Returns:
            A KordacResult object.
        """
        kordac_extension = KordacExtension(tags, html_templates)
        converter = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            mdx_math.MathExtension(enable_dollar_delimiter=True),
            kordac_extension])
        kordac_extension.heading = None
        html = converter.convert(text)
        result = KordacResult(
            html=html,
            heading=kordac_extension.page_heading
        )
        return result


class KordacResult(object):
    """Object created by Kordac containing the result data
    after a conversion by run.
    """

    def __init__(self, html=None, heading=None):
        """Create a KordacResult object.

        Args:
            html: A string of HTML text.
            heading: The first heading encountered when converting.
        """
        self.html = html
        self.heading = heading
