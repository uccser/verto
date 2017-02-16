import markdown
from kordac.KordacExtension import KordacExtension

DEFAULT_PROCESSORS = {
    'save-title',
    'heading',
    'comment',
    'button-link',
    'panel',
    'video',
    'image',
    'relative-link',
    'interactive',
    'glossary-link'
}

class Kordac(object):
    """A converter object for converting markdown
    with complex elements to HTML.
    """

    def __init__(self, processors=DEFAULT_PROCESSORS, html_templates={}, extensions=[]):
        """Creates a Kordac object.

        Args:
            processors: A set of processor names given as strings for which
                their processors are enabled. If given, all other
                processors are skipped.
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for processors. Dictionary contains
                processor names given as a string as keys mapping HTML strings
                as values.
                eg: {'image': '<img src={{ source }}>'}
            extensions: A list of extra extensions to run on the
                markdown package.
        """
        self.processors = set(processors)
        self.html_templates = html_templates
        self.extensions = extensions
        self.create_converter()

    def create_converter(self):
        """Create the Kordac extension and converter for future use."""
        self.kordac_extension = KordacExtension(
            processors=self.processors,
            html_templates=self.html_templates
        )
        all_extensions = self.extensions + [self.kordac_extension]
        self.converter = markdown.Markdown(extensions=all_extensions)

    def convert(self, text):
        """Return a KordacResult object after converting
        the given markdown string.

        Args:
            text: A string of Markdown text to be converted.

        Returns:
            A KordacResult object.
        """
        self.kordac_extension.clear_saved_data()
        html_string = self.converter.convert(text)
        result = KordacResult(
            html_string=html_string,
            title=self.kordac_extension.title,
            required_files=self.kordac_extension.required_files
        )
        return result

    def update_templates(self, html_templates):
        """Update the template dictionary with the given dictionary
        of templates, while leaving all other HTML templates (including
        any custom set templates) untouched. The updated dictionary
        will be used for converting from this point onwards.

        Args:
            html_templates: A dictionary of HTML templates to override
                existing HTML templates for processors. Dictionary contains
                processor names given as a string as keys mapping HTML strings
                as values.
                eg: {'image': '<img src={{ source }}>'}
        """
        self.html_templates.update(html_templates)
        self.create_converter()

    def default_templates(self):
        """Set the template dictionary to it's original values."""
        self.html_templates = {}
        self.create_converter()

    def processor_defaults(self):
        """Returns a copy of the default processor set.

        Returns:
            A set of default processor names as strings.
        """
        return DEFAULT_PROCESSORS.copy()

    def update_processors(self, processors=DEFAULT_PROCESSORS):
        """Update the processors used for conversion with the given set.
        The updated set will be used for converting from this point
        onwards. If parameter is empty, default processors will be used.

        Args:
            processors: A set of processor names given as strings for which
                their processors are enabled. If given, all other
                processors are skipped.
        """
        self.processors = set(processors)
        self.create_converter()

class KordacResult(object):
    """Object created by Kordac containing the result data
    after a conversion by run.
    """

    def __init__(self, html_string, title, required_files):
        """Create a KordacResult object.

        Args:
            html_string: A string of HTML text.
            title: The first heading encountered when converting.
            required_files: Dictionary of required file types to sets of paths.
        """
        self.html_string = html_string
        self.title = title
        self.required_files = required_files
