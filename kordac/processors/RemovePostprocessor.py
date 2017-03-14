from markdown.postprocessors import Postprocessor


class RemovePostprocessor(Postprocessor):
    ''' Parses the output document and removes all remove html tags
    (i.e. <remove> or </remove>) keeping the body of said tags. This
    allows for the returning of illegal html for further processing.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text):
        '''
        Args:
            text: A string of the document.
        Returns:
            The document text with all remove tag removed.
        '''
        return text.replace('<remove>', '').replace('</remove>', '')
