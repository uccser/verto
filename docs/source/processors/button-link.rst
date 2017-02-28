Button Link
#######################################

**Processor name:** ``button-link``

You can create a link on a button using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``link`` - The URL to link to.

    - If the given link is a relative, a placeholder for Django to prepend the root is outputted.
    - If the ``file`` parameter is set to ``yes``, then the link will be rendered with a Django static command. See ``file`` parameter below.
- ``text`` - Text to display on the button.

Optional Tag Parameters
***************************************

- ``file`` - If set to ``yes`` the link will be rendered with a Django static command. This is useful if you wish to create a button link to a file or image.

    - For example, the link ``files/python-sort-example.py`` would be rendered as ``{% static 'files/python-sort-example.py' %}``. This can be overriden, see the override section below.:

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/button-link.html
    :language: css+jinja

**Example 1**

Using the following tag:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_basic_usage_expected.html
    :language: html

**Example 2**

Using the following tag:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_file_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_file_usage_expected.html
    :language: css+jinja

Overriding HTML for Button Link
***************************************

When overriding the HTML for button links, the following Jinja2 placeholders are available:

- ``{{ link }}`` - The URL.
- ``{{ text }}`` - Text to display on the button.

If the ``file`` parameter is set to ``yes``, the link is passed through the ``relative-image-link.html`` template. The default HTML for relative images is:

.. literalinclude:: ../../../kordac/html-templates/relative-file-link.html
  :language: css+jinja

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_override_html_expected.html
    :language: html
