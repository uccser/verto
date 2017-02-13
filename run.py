import kordac

for chapter in ['algorithms', 'introduction']:
    with open('kordac/{}.md'.format(chapter), 'r') as f:
        s = f.read()
        converter = kordac.Kordac()
        # result = converter.run(s, tags=['heading'])
        result = converter.run(s)
    with open('kordac/output/{}.html'.format(chapter), 'w', encoding='utf8') as f:
        f.write(result.html_string)
