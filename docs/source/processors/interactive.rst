Interactive
#######################################

**Processor name:** ``interactive``

The term *interactive* was defined in the `Computer Science Field Guide`_ to
describe an interactive component of a page.
This could be educational game or demostration that is created in HTML, CSS,
and JS.
Interactives can be small examples to display within the text (for example:
`animations comparing sorting algorithms`_) to larger interactives that require
a whole page to view (for example: `viewing pixels of an image`_.).

By using the interactive tag, Kordac can include or link to an interactive
within a page. Kordac does not directly include the interactive, but creates
Django commands for a Django system to render the interactive or link to
interactive as requested.

You can include an interactive using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_in_page_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``name`` - The name to the interactive to include/link to.
- ``type`` - Sets the way the interactive is included in the page. Must be set
  to one of the following values:

    - ``in-page`` - The interactive is included in the page by including the
      HTML (this is the preferred method for including an interactive on a
      page).
    - ``whole-page`` - Creates a link to the interactive displayed on a
      separate page (this is the preferred method for including an interactive
      on a separate page). The link shows a thumbnail of the interactive with
      text (the text is set using the ``text`` parameter).
      By default, the thumbnail should be a ``thumbnail.png`` file found
      within the interactive folder.
    - ``iframe`` - The interactive is included in the page by embedding using
      an iframe. This is used if the interactive is included multiple times on
      the page to avoid conflicts in JavaScript/CSS.

Optional Tag Parameters
***************************************

- ``text`` (used with ``whole-page`` value) - Sets the text for the interactive
  link. If no text is given, the link uses the text ``Click to load
  {{ name }}``.
- ``parameters`` (used with ``whole-page`` and ``iframe`` values) - Adds the parameters
  to interactive link. For example: ``digits=5&start=BBBBB``. Do not include
  the ``?`` at the start, as this is already included in the output.
- ``thumbnail`` (optional - used with ``whole-page`` value) - Displays an
  alternative thumbnail for the interactive. When not provided, it defaults to
  the ``thumbnail.png`` image within the interactive's folder.

  - If the ``thumbnail`` value provided is an relative link (a link that
    doesn't start with ``http:``), the link will be rendered with a Django
    static command. For example, the link:

    .. code-block:: none

      binary-cards/thumbnail-2.png

    would be rendered as:

    .. code-block:: none

      {% static 'binary-cards/thumbnail-2.png' %}

    This can be overriden, see the override section below.
  - Each ``thumbnail`` provided is added to the ``images`` set in required
    files stored by Kordac.
    The set of filepaths can be accessed after conversion,
    see :ref:`accessing_kordac_data`.

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/interactive.html
    :language: css+jinja

Examples
***************************************

**in-page example**

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_in_page_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_in_page_usage_expected.html
    :language: html

**whole-page example**

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_whole_page_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_whole_page_usage_expected.html
    :language: html

**iframe example**

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_iframe_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_iframe_usage_expected.html
    :language: html

Overriding HTML for Interactives
***************************************

When overriding the HTML for interactives, the following Jinja2 placeholders are available:

- ``{{ name }}`` - The slug name of the interactive to include/link to.
- ``{{ text }}`` - The text to to display to a link to a ``whole-page``
  interactive.
- ``{{ parameters }}`` - GET parameters to append to the interactive link.
- ``{{ file_path }}`` - The location for the path to the thumbnail image.

If the ``file_path`` provided is an relative link, the link is passed through the ``relative-image-link.html`` template.
The default HTML for relative images is:

.. literalinclude:: ../../../kordac/html-templates/relative-file-link.html
  :language: css+jinja

**Example**

This example creates a link to ``whole-page`` interactives without a
thumbnail.

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_override_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/interactive/doc_example_override_html_expected.html
   :language: html

.. _Computer Science Field Guide: https://github.com/uccser/cs-field-guide
.. _animations comparing sorting algorithms: http://www.csfieldguide.org.nz/en/interactives/sorting-algorithm-comparison/index.html
.. _viewing pixels of an image: http://www.csfieldguide.org.nz/en/interactives/pixel-viewer/index.html
