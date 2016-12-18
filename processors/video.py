from markdown.blockprocessors import BlockProcessor
import re
from processors.utils import parse_argument, centre_html
from markdown.util import etree

YOUTUBE_SRC = "http://www.youtube.com/embed/{0}?rel=0"
VIMEO_SRC = "http://player.vimeo.com/video/{0}"

VIDEO_TEMPLATE ="""
<div class='video-container no-controls'>
    <iframe src='{source}' frameborder='0' allowfullscreen='allowfullscreen'></iframe>
</div>"""


class VideoBlockProcessor(BlockProcessor):
    p = re.compile('^\{video (?P<args>[^\}]*)\}')

    def test(self, parent, block):
        return self.p.match(block) is not None

    def run(self, parent, blocks):
        match = self.p.match(blocks.pop(0))
        arguments = match.group('args')
        url = parse_argument('url', arguments)
        (video_type, video_identifier) = extract_video_identifier(url, match)
        if url:
            if video_type:
                if video_type == 'youtube':
                    source_link = YOUTUBE_SRC.format(video_identifier)
                elif video_type == 'vimeo':
                    source_link = VIMEO_SRC.format(video_identifier)
                node = etree.fromstring(VIDEO_TEMPLATE.format(source=source_link))
                parent.append(centre_html(node, 10))


def extract_video_identifier(video_link, match):
    """Returns the indentifier from a given URL"""
    if "youtu.be" in video_link or "youtube.com/embed" in video_link:
        identifier = ('youtube', video_link.split('/')[-1])
    elif "youtube.com" in video_link:
        start_pos = video_link.find("v=") + 2
        end_pos = video_link.find("&");
        if end_pos == -1:
            identifier = ('youtube', video_link[start_pos:])
        else:
            identifier = ('youtube', video_link[start_pos:end_pos])
    elif "vimeo" in video_link:
        identifier = ('vimeo', video_link.split('/')[-1])
    else:
        identifier = (None,'')
    return identifier
