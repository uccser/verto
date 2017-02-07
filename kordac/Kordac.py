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
            tags: A list of tag names given as strings for which
                their processors are enabled. If given, all other
                processors are skipped.
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for tags. Dictionary contains
                tag names given as a string as keys mapping HTML strings
                as values.
                eg: {'image': '<img src={{ source }}>'}

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
        html_string = converter.convert(text)
        result = KordacResult(
            html_string=html_string,
            heading=kordac_extension.page_heading
        )
        return result


class KordacResult(object):
    """Object created by Kordac containing the result data
    after a conversion by run.
    """

    def __init__(self, html_string=None, heading=None):
        """Create a KordacResult object.

        Args:
            html_string: A string of HTML text.
            heading: The first heading encountered when converting.
        """
        self.html_string = html_string
        self.heading = heading
