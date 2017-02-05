from Kordac import Kordac

for chapter in ['algorithms', 'introduction']:
    with open("{}.md".format(chapter), 'r') as f:
        s = f.read()
        converted = Kordac().run(s)
    with open("output/{}.html".format(chapter), 'w', encoding='utf8') as f:
        f.write(converted.html_string)

