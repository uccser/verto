import markdown
import mdx_math
import jinja2
from csfg_extension import CSFGExtension

def main():
    html = None
    with open("test_input.md", 'r') as f:
        s = f.read()
        ext = CSFGExtension()
        html = markdown.markdown(s, extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            mdx_math.MathExtension(enable_dollar_delimiter=True),
            ext])

    with open("template.html") as f:
        template = f.read()

    with open("output/output.html", 'w') as f:
        template = jinja2.Template(template)
        f.write(template.render(content=html))

main()
