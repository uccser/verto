from html.parser import HTMLParser
from markdown.util import etree

class VertoHtmlParser(HTMLParser):
    ''' Used to convert an HTML string into an ElementTree. Since this
    is not defaultly supported by fromstring (XML only).
    '''

    VOID_ELEMENTS = [
        'area', 'base', 'br', 'command', 'embed', 'hr', 'img', 'input',
        'link', 'input', 'link', 'meta', 'param', 'source'
    ]

    OPTIONALLY_CLOSE_ELEMENTS = [
        'body', 'colgroup', 'dd', 'dt', 'head', 'html', 'li', 'optgroup',
        'option', 'p', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'
    ]

    def __init__(self, *args, **kwargs):
        '''Create a new parser.
        '''
        super().__init__(convert_charrefs=True, *args, **kwargs)
        self.root = None
        self.closed = False

    def get_root(self):
        '''Gets the root element after parsing.
        Returns:
            An etree Element of the root node.
        Raises:
            Error: If no root has been found or the parser
              has not been closed yet.
        '''
        if self.root is None or not self.closed:
            raise Exception("TODO")
        return self.root

    def close(self):
        '''Force processing of all buffered data as if it were
        followed by an end-of-file mark.
        '''
        self.closed = True
        super().close()

    def reset(self):
        '''Reset the instance. Loses all unprocessed data.
        '''
        self.root = None
        self.closed = False
        super().reset()

    def handle_starttag(self, tag, attrs):
        '''This method is called to handle the start of a tag
        (e.g. `<div id="main">`).

        Args:
            tag: The name of the tag (converted to lowercase).
            attrs: A list of tuples (name, value) where the name is
              converted to lowercase and qoutes on the value have
              been removed.
        '''
        print("Encountered a start tag :", tag)

    def handle_endtag(self, tag):
        '''This method is called to handle the end tag of an
        element (e.g. `</div>`).

        Args:
            tag: The name of the tag (converted to lowercase).
        '''
        print("Encountered an end tag :", tag)

    def handle_startendtag(self, tag, attrs):
        '''Similar to handle_starttag(), but called when the parser
        encounters an XHTML-style empty tag (<img ... />).

        Args:
            tag: The name of the tag (converted to lowercase).
            attrs: A list of tuples (name, value) where the name is
              converted to lowercase and qoutes on the value have
              been removed.
        '''
        print("Encountered an startend tag :", tag)
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        '''This method is called to process arbitrary data (e.g.
        text nodes and the content of <script>...</script> and
        <style>...</style>).

        Args:
            data: The content between the tags.
        '''
        print("Encountered some data :", data)


    def handle_comment(self, data):
        '''This method is called when a comment is encountered
        (e.g. <!--comment-->).

        Note:
            The content of Internet Explorer conditional comments
            (condcoms) will also be sent to this method.
        Args:
            data: The string of the comment.
        '''
        print("Encountered a comment tag :", data)

    def handle_entityref(self, name):
        '''This method is called to process a named character reference
        of the form &name; (e.g. &gt;).

        Note:
            This function should never be called, since the HTMLParser
            is initialized with convert_charrefs as True.
        Args:
            name: The string of entity with ampersand and semicolon
              removed.
        '''
        super().handle_entityref(data)

    def handle_charref(self, name):
        '''This method is called to process decimal and hexadecimal
        numeric character references of the form `&#NNN;` and
        `&#xNNN;`.

        Note:
            This function should never be called, since the HTMLParser
            is initialized with convert_charrefs as True.
        Args:
            name: The string of the decimal or hexadecimal of the char.
        '''
        super().handle_charref(data)

    def unknown_decl(self, data):
        '''This method is called when an unrecognized declaration is read by the parser.

        Args:
            data: The entire contents of the declaration inside
              the `<[!...]>` markup.
        '''
        super().unknown_decl(data)

    def handle_decl(self, decl):
        '''This method is called to handle an HTML doctype declaration
        (e.g. <!DOCTYPE html>).

        Args:
            decl: The entire contents of the declaration inside
              the `<!...>` markup.
        '''
        raise NotImplementedError("HTML declarations are not supported.")

    def handle_pi(self, data):
        '''Method called when a processing instruction is encountered.
        (e.g. `<? ...>`).

        Note:
            An XHTML processing instruction using the trailing '?' will
            cause the '?' to be included in data.
        Args:
            data: The entire processing instruction as a string.
        '''
        raise NotImplementedError("Processing instructions are not supported.")
