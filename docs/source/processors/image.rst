Image
#######################################

**Processor name:** ``image-tag`` and ``image-container``

You can include an image using the following text tag:

.. code-block:: none

    {image file-path="http://placehold.it/350x150" caption="true"}

    This is the caption text.

    {image end}

The caption is the first block of text within the image block.
It is within the block rather than given as a parameter to allow translation systems to easily identify which text should be translated.

If a caption is not needed, an end tag is not required (see example below).

.. code-block:: none

    {image file-path="http://placehold.it/350x150" caption="false"}


Required Tag Parameters
***************************************

- ``file-path`` - The path to the image.

    - Each file-path provided is added to the ``images`` set in required files stored by Verto. The set of filepaths can be accessed after conversion, see :ref:`accessing_verto_data`.
    - **Note:** If the given link is a relative (a link that doesn't start with ``http:``), the link will be rendered with a Django static command. For example, the link ``images/example.png`` would be rendered as ``{% static 'images/example.png' %}`` This can be overriden, see the override section below.

Optional Tag Parameters
***************************************

- ``alt`` - Description text of the image used when an image is not displayed, or can be read when using a screen reader (for those with reading difficulties).

- ``caption`` - Boolean flag to indicate whether the image should display a caption.

    - If given as ``true``, the the subtitle is the first block of text with the image block.

- ``caption-link`` (requires caption parameter) - Converts the caption text into a link to the given caption link URL.

- ``source`` (optional) - Adds the text 'Source' under the image with a link to the given source URL. Displays after the caption if a caption is given.

- ``alignment`` - Valid values are 'left', 'center', or 'right'. Providing one of these values Will add CSS classes to the image for alignment.

- ``hover-text`` - Additional text to be displayed when the user hovers their cursor over the image (note this won't appear on touch devices so use sparingly).

The default HTML for image is:

.. literalinclude:: ../../../verto/html-templates/image.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_basic_usage_expected.html
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

If the ``file_path`` provided is a relative link, the link is passed through the ``relative-file-link.html`` template.
The default HTML for relative images is:

.. literalinclude:: ../../../verto/html-templates/relative-file-link.html
  :language: css+jinja

**Example 1**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_override_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_override_html_expected.html
   :language: html

**Example 2**

If you know all relative images are located within a specific folder, you could change the ``relative-file-link.html`` template.

For example, providing the following HTML for ``image.html``:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_2_override_html_template.html
   :language: css+jinja

and providing the following HTML for ``relative-file-link.html``:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_2_override_link_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_2_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/image/doc_example_2_override_html_expected.html
   :language: html
