from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from kordac.processors.errors.NoSourceLinkError import NoSourceLinkError
from kordac.processors.utils import parse_argument
import re


class VideoBlockProcessor(BlockProcessor):

    def __init__(self, ext, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processor = 'video'
        self.pattern = re.compile(ext.processor_patterns[self.processor]['pattern'])
        self.youtube_template = ext.jinja_templates['video-youtube']
        self.vimeo_template = ext.jinja_templates['video-vimeo']
        self.template = ext.jinja_templates[self.processor]

    def test(self, parent, block):
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):

        block = blocks.pop(0)
        match = self.pattern.search(block) # NTS why not search?

        arguments = match.group('args') # NTS what other arguments will there be?
        url = parse_argument('url', arguments)

        (video_type, video_identifier) = self.extract_video_identifier(url, match)

        context = dict()
        context['video_identifier'] = video_identifier

        source_link = ''
        if url and video_type:
            if video_type == 'youtube':
                context['source_link'] = self.youtube_template.render(context)
            elif video_type == 'vimeo':
                context['source_link'] = self.vimeo_template.render(context)

        if not context['source_link']:
            raise NoSourceLinkError(block, url, 'invalid video source link')


        html_string = self.template.render(context)

        node = etree.fromstring(html_string)
        parent.append(node)


    def extract_video_identifier(self, video_url, match):
        '''Returns the indentifier from a given URL'''

        if re.match('.*?youtu\.{0,1}be.com', video_url) is not None: # is a youtube url
            video_url = re.sub(r'(.*?)(\?rel=0)', r'\g<1>', video_url)

            if 'youtu.be' in video_url or 'youtube.com/embed' in video_url:
                video_query = video_url.split('/')[-1]
            elif 'youtube.com' in video_url:
                start_pos = video_url.find('v=') + 2
                end_pos = video_url.find('&');
                if end_pos == -1:
                    end_pos = len(video_url)
                video_query = video_url[start_pos:end_pos]
                identifier = ('youtube', video_query)

            return('youtube', video_query)

        elif 'vimeo' in video_url:
            video_query = video_url.split('/')[-1]
            return ('vimeo', video_query)

        return (None, '')

