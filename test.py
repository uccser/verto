from kordac import *
extensions = [
    #'markdown.extensions.codehilite',
    'markdown.extensions.fenced_code',
]
k = Kordac(extensions=extensions)
with open('kordac/tests/assets/scratch/doc_example_basic_usage.md', 'r') as f:
#with open('test.md', 'r') as f:
    t = f.read()
r = k.convert(t)
print(r.html_string)
print()
print(r.required_files['scratch_images'])
