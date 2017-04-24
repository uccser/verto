from markdown.util import etree
import re


class HtmlSerializer(object):
    '''Converts an element tree object which is HTML into
    a string.
    '''

    COMMENT_PATTERN = r'<!--(?P<start_condition>.*?)&gt;(?P<content>.*?)&lt;!(?P<end_condition>.*?)-->'

    @staticmethod
    def tostring(root):
        '''Converts an etree into a string.

        Args:
            root: An Element from the ElementTree library.
        Returns:
            A string of the serialized HTML tree.
        '''
        string = etree.tostring(root, encoding='unicode', method='html')

        def unescape_comment(matchobj):
            return r'<!--{}>{}<!{}-->'.format(
                matchobj.group('start_condition'),
                matchobj.group('content'),
                matchobj.group('end_condition'))
        string = re.sub(HtmlSerializer.COMMENT_PATTERN, unescape_comment, string, flags=re.DOTALL)
        return string
