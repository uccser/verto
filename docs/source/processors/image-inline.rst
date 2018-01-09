Inline Image
#######################################

**Processor name:** ``image-inline``

.. note::

    The inline image tag allows for the use of images inside tables, *etc* without causing style errors. The tag functions almost exactly the same as the ``image`` tag except for the alignment argument.

You can include an inline image using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``file-path`` - The path to the image.

    - Each file-path provided is added to the ``images`` set in required files stored by Verto. The set of filepaths can be accessed after conversion, see :ref:`accessing_verto_data`.
    - **Note:** If the given link is a relative (a link that doesn't start with ``http:``), the link will be rendered with a Django static command. For example, the link ``images/example.png`` would be rendered as ``{% static 'images/example.png' %}`` This can be overriden, see the override section below.

Optional Tag Parameters
***************************************

- ``alt`` - Description text of the image used when an image is not displayed, or can be read when using a screen reader (for those with reading difficulties).
- ``caption`` - Lists the given text as a caption under the image.
- ``caption-link`` (requires caption parameter) - Converts the caption text into a link to the given caption link URL.
- ``source`` (optional) - Adds the text 'Source' under the image with a link to the given source URL. Displays after the caption if a caption is given.
- ``hover-text`` - Additional text to be displayed when the user hovers their cursor over the image (note this won't appear on touch devices so use sparingly).

The default HTML for image is:

.. literalinclude:: ../../../verto/html-templates/image-inline.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_basic_usage_expected.html
    :language: html

Overriding HTML for Images
***************************************

When overriding the HTML for images, the following Jinja2 placeholders are available:

- ``{{ full_file_path }}`` - The location for the path to the URL.
- ``{{ alt }}`` - The alternative text for the image.
- ``{{ hover_text }}`` - The text to display when the user hovers over the image (see `image title attribute <https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title>`_).
- ``{{ caption }}`` - The text for the image caption.
- ``{{ caption_link }}`` - The URL for the caption link .
- ``{{ source_link }}`` - The URL for the source .
- ``{{ file_relative }}`` - If the ``full_file_path`` is a relative link, this is the boolean value ``True``, otherwise ``False``.

    If ``{{ file_relative }}`` is ``True``, the following placeholders are also available to allow finer control of output of relative images (see *Example 2* below):

    - ``{{ file_path }}`` - The file path of the image, with file extension removed.
    - ``{{ file_extension }}`` - The file extension for the image.
    - ``{{ file_width_value }}`` - If the file name of the image ends in a width suffix (for example: ``apple@200px.png``), this is the numerical width value as an integer (in the example before: ``200``).
    - ``{{ file_width_unit }}`` - If the file name of the image ends in a width suffix (for example: ``apple@200px.png``), this is the width unit (in the example before: ``px``).

**Example 1**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_override_html_expected.html
    :language: html

**Example 2**

This is an example of using the ``scrset`` attribute for relative images.

The following HTML for ``image.html``:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_2_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_2_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/image-inline/doc_example_2_override_html_expected.html
    :language: html
