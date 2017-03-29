from markdown.postprocessors import Postprocessor

class RemovePostprocessor(Postprocessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, text):
        return text.replace('<remove>', '').replace('</remove>', '')
