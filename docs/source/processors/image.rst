Image
#######################################

**Processor name:** ``image``

You can include an image using the following text tag:

.. code-block:: none

    {image file_path="http://placehold.it/350x150"}

Required Tag Parameters
***************************************

- ``file_path`` - The path to the image.

    - Each file_path provided is added to the set of 'required files' stored by Kordac. The list of filepaths can be accessed after conversion.
    - **Note:** If the given link is a relative (a link that doesn't start with ``http:``), the link will be rendered with a Django static command. For example, the link ``images/example.png`` would be rendered as ``{% static 'images/example.png' %}`` This can be overriden, see the override section below.

Optional Tag Parameters
***************************************

- ``alt`` - Description text of the image used when an image is not displayed, or can be read when using a screen reader (for those with reading difficulties).
- ``caption`` - Lists the given text as a caption under the image.
- ``caption-link`` (requires caption parameter) - Converts the caption text into a link to the given caption link URL.
- ``source`` (optional) - Adds the text 'Source' under the image with a link to the given source URL. Displays after the caption if a caption is given.
- ``alignment`` - Valid values are 'left', 'center', or 'right'. Providing one of these values Will add CSS classes to the image for alignment.
- ``hover-text`` - Additional text to be displayed when the user hovers their cursor over the image (note this won't appear on touch devices so use sparingly).

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/image.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Images
***************************************

When overriding the HTML for images, the following Jinja2 placeholders are available:

- ``{{ file_path }}`` - The location for the path to the URL.
- ``{{ alt }}`` - The alternative text for the image.
- ``{{ hover_text }}`` - The text to display when the user hovers over the image (see `image title attribute <https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title>`_).
- ``{{ alignment }}`` - The location to add extra CSS classes for alignment.
- ``{{ caption }}`` - The text for the image caption.
- ``{{ caption_link }}`` - The URL for the caption link .
- ``{{ source_link }}`` - The URL for the source .

If the ``file_path`` provided is an relative link, the link is passed through the ``relative-image-link.html`` template.
The default HTML for relative images is:

.. literalinclude:: ../../../kordac/html-templates/relative-image-link.html
  :language: css+jinja

**Example 1**

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_override_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_override_html_expected.html
   :language: html

**Example 2**

If you know all relative images are located within a specific folder, you could change the ``relative-image-link.html`` template.

For example, providing the following HTML for ``image.html``:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_2_override_html_template.html
   :language: css+jinja

and providing the following HTML for ``relative-image-link.html``:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_2_override_link_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_2_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/image/doc_example_2_override_html_expected.html
   :language: html