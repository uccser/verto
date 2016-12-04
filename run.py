import markdown
import mdx_math
from test import CSFGExtension

def main():
    html = None
    for chapter in ['algorithms', 'introduction']:
        with open("{}.md".format(chapter), 'r') as f:
            s = f.read()
            ext = CSFGExtension()
            html = markdown.markdown(s, extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.sane_lists',
                mdx_math.MathExtension(enable_dollar_delimiter=True),
                ext])

        with open("output/{}.html".format(chapter), 'w', encoding='utf8') as f:
            f.write(html)

if __name__ == "__main__":
    main()
