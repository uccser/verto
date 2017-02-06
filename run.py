import kordac

for chapter in ['algorithms', 'introduction']:
    with open('kordac/{}.md'.format(chapter), 'r') as f:
        s = f.read()
        converted = kordac.Kordac().run(s)
    with open('kordac/output/{}.html'.format(chapter), 'w', encoding='utf8') as f:
        f.write(converted.html_string)
