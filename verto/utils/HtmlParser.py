import html.parser
from verto.errors.HtmlParseError import HtmlParseError
from markdown.util import etree


class HtmlParser(html.parser.HTMLParser):
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
        self.stack = []

    def get_root(self):
        '''Gets the root element after parsing.

        Returns:
            An etree Element of the root node.
        Raises:
            Error: If no root has been found or the parser
              has not been closed yet.
        '''
        if self.root is None or not self.closed:
            raise AttributeError("Operations out of order: root accessed before created.")
        return self.root

    def feed(self, data):
        '''Feed some text to the parser.

        Args:
            data: The text to feed to the parser.
        Returns:
            Itself.
        '''
        super().feed(data)
        return self

    def close(self):
        '''Force processing of all buffered data as if it were
        followed by an end-of-file mark.

        Returns:
            Itself.
        '''
        for element in self.stack:
            if element.tag not in HtmlParser.OPTIONALLY_CLOSE_ELEMENTS:
                line, pos = self.getpos()
                msg = "Trying to implicitly close a normal element ({}).".format(element.tag)
                raise HtmlParseError(line, pos, msg)
        self.closed = True
        super().close()
        return self

    def reset(self):
        '''Reset the instance. Loses all unprocessed data.
        '''
        self.root = None
        self.closed = False
        self.stack = []
        super().reset()

    def add_element(self, element):
        '''Adds an element to the element tree.

        Args:
            element: An etree Element to append to the element tree.
        '''
        if self.root is None and len(self.stack) <= 0:
            self.root = element
        elif self.root is not None and len(self.stack) <= 0:
            line, pos = self.getpos()
            raise HtmlParseError(line, pos, "Secondary root node found.")
        else:
            self.stack[-1].append(element)

        if element.tag not in HtmlParser.VOID_ELEMENTS and element.tag != etree.Comment:
            self.stack.append(element)

    def handle_starttag(self, tag, attrs):
        '''This method is called to handle the start of a tag
        (e.g. `<div id="main">`).

        Args:
            tag: The name of the tag (converted to lowercase).
            attrs: A list of tuples (name, value) where the name is
              converted to lowercase and qoutes on the value have
              been removed.
        '''
        element = etree.Element(tag, dict(attrs))
        self.add_element(element)

    def handle_endtag(self, tag):
        '''This method is called to handle the end tag of an
        element (e.g. `</div>`).

        Args:
            tag: The name of the tag (converted to lowercase).
        '''
        if tag not in HtmlParser.VOID_ELEMENTS:
            found = False
            while not found and len(self.stack) > 0:
                element = self.stack.pop()
                if element.tag == tag:
                    found = True
                elif element.tag not in HtmlParser.OPTIONALLY_CLOSE_ELEMENTS:
                    line, pos = self.getpos()
                    raise HtmlParseError(line, pos, "Trying to implicitly close a normal element.")

            if not found:
                line, pos = self.getpos()
                raise HtmlParseError(line, pos, "Trying to close an unopened element.")

    def handle_startendtag(self, tag, attrs):
        '''Similar to handle_starttag(), but called when the parser
        encounters an XHTML-style empty tag (<img ... />).

        Args:
            tag: The name of the tag (converted to lowercase).
            attrs: A list of tuples (name, value) where the name is
              converted to lowercase and qoutes on the value have
              been removed.
        '''
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        '''This method is called to process arbitrary data (e.g.
        text nodes and the content of <script>...</script> and
        <style>...</style>).

        Args:
            data: The content between the tags.
        '''
        if len(self.stack) <= 0:
            if data.strip() != '':
                line, pos = self.getpos()
                raise HtmlParseError(line, pos, "Data outside of the HTML tree.")
        else:
            sibling = list(self.stack[-1])[-1] if list(self.stack[-1]) else None
            if sibling is not None:
                sibling.tail = (sibling.tail or '') + data
            else:
                self.stack[-1].text = (self.stack[-1].text or '') + data

    def handle_comment(self, data):
        '''This method is called when a comment is encountered
        (e.g. <!--comment-->).

        Note:
            The content of Internet Explorer conditional comments
            (condcoms) will also be sent to this method.
        Args:
            data: The string of the comment.
        '''
        element = etree.Comment(data)
        self.add_element(element)

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
        super().handle_entityref(name)

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
        super().handle_charref(name)

    def unknown_decl(self, data):
        '''This method is called when an unrecognized declaration is read by the parser.

        Args:
            data: The entire contents of the declaration inside
              the `<[!...]>` markup.
        '''
        raise NotImplementedError("Unknown declarations are not supported.")

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
