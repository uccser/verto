Video
#######################################

**Processor name:** ``video``

You can include an video using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_basic_usage.md
  :language: none

Required Tag Parameters
***************************************

- ``url`` - The video embed URL for the video. Currently only YouTube and Vimeo videos are supported.

  - **For YouTube videos:** Provide the URL in any of the following formats and Verto will automatically create the embed link. YouTube videos have related videos hidden at video end by default.

    - ``https://www.youtube.com/watch?v=dQw4w9WgXcQ`` - Standard URL
    - ``https://youtu.be/dQw4w9WgXcQ`` - Shortened URL
    - ``https://www.youtube.com/embed/dQw4w9WgXcQ`` - Embed URL

  - **For Vimeo videos:** Provide the URL in any of the following formats and Verto will automatically create the embed link.

    - ``https://vimeo.com/94502406`` - Standard URL
    - ``https://player.vimeo.com/video/94502406``- Embed URL

The default HTML for a video is:

.. literalinclude:: ../../../verto/html-templates/video.html
  :language: css+jinja

If the URL provided is YouTube video, the video identifier is extracted and is passed through the ``video-youtube.html`` template:

.. literalinclude:: ../../../verto/html-templates/video-youtube.html
  :language: css+jinja

If the URL provided is YouTube video, the video identifier is extracted and is passed through the ``video-vimeo.html`` template:

.. literalinclude:: ../../../verto/html-templates/video-vimeo.html
  :language: css+jinja

**Example**

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Videos
***************************************

When overriding the HTML for videos, the following Jinja2 placeholders are available:

- ``{{ video_url }}`` - The URL of the video to be embedded.

In the ``video-youtube.html``, the following Jinja2 placeholders are available:

- ``{{ youtube_identifier }}`` - The identifer of the YouTube video to be embedded.

In the ``video-vimeo.html``, the following Jinja2 placeholders are available:

- ``{{ vimeo_identifier }}`` - The identifer of the Vimeo video to be embedded.

**Example**

For example, providing the following HTML for ``video-youtube.html``:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_override_html_youtube_template.html
 :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_override_html.md
 :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/video/doc_example_override_html_expected.html
 :language: html
