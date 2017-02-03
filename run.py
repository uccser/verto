import markdown
import mdx_math
from Kordac import KordacExtension
import sys


class Kordac():

    def run(self, md_string):
        self.heading = 'I am a heading'
        self.required_files = {}
        self.html_string = ''
        html = None
        ext = KordacExtension()
        converter = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            mdx_math.MathExtension(enable_dollar_delimiter=True),
            ext])

        self.html_string = converter.convert(md_string)
        self.heading = ext.page_heading

        return self

hello = Kordac()
something = hello.run('this is a test string')
print(something.html_string)
print(something.heading)

        # for chapter in ['algorithms', 'introduction']:
            # with open("{}.md".format(chapter), 'r') as f:
                # s = f.read()

                # html = converter.convert(s)

            # with open("output/{}.html".format(chapter), 'w', encoding='utf8') as f:
                # f.write(html)


# if __name__ == "__main__":
    # main()

