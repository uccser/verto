import markdown
import jinja2
from csfg_extension import CSFGExtension

def main():
    html = None
    with open("test_input.md", 'r') as f:
        s = f.read()
        html = markdown.markdown(s, extensions=['markdown.extensions.fenced_code','markdown.extensions.codehilite', CSFGExtension()])

    with open("template.html") as f:
        template = f.read()
        
    with open("output/output.html", 'w') as f:
        template = jinja2.Template(template)
        f.write(template.render(content=html))

main()
