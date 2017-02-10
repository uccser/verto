import markdown
import mdx_math
from kordac.KordacExtension import KordacExtension

class Kordac(object):
    """A converter object for converting markdown
    with complex tags to HTML.
    """

    def __init__(self, tags=[], html_templates={}, extensions=[]):
        """Creates a Kordac object.

        Args:
            tags: A list of tag names given as strings for which
                their processors are enabled. If given, all other
                processors are skipped.
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for tags. Dictionary contains
                tag names given as a string as keys mapping HTML strings
                as values.
                eg: {'image': '<img src={{ source }}>'}
            extensions: A list of extra extensions to run on the
                markdown package.
        """
        self.tags = tags
        self.html_templates = html_templates
        self.extensions = extensions
        self.create_converter()

    def create_converter(self):
        """Create the Kordac extension and converter for future use."""
        self.kordac_extension = KordacExtension(
            tags=self.tags,
            html_templates=self.html_templates
        )
        all_extensions = self.extensions + [self.kordac_extension]
        self.converter = markdown.Markdown(extensions=all_extensions)

    def run(self, text):
        """Return a KordacResult object after converting
        the given markdown string.

        Args:
            text: A string of Markdown text to be converted.

        Returns:
            A KordacResult object.
        """
        self.kordac_extension.reset()
        html_string = self.converter.convert(text)
        result = KordacResult(
            html_string=html_string,
            heading=self.kordac_extension.page_heading
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
