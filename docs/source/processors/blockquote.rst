Blockquote
#######################################

**Processor name:** ``blockquote``

You can include an blockquote using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_basic_usage.md
    :language: none

Optional Tag Parameters
***************************************

- ``footer`` - Boolean flag to indicate whether the blockquote contains a footer.

    - If given as ``true``, then the last line should start with ``- `` to show it's the footer.

- ``source`` - Sets the ``cite`` parameter of the ``blockquote`` element.

- ``alignment`` - Valid values are 'left', 'center', or 'right'. Providing one of these values Will add CSS classes to the image for alignment.

The default HTML for a panel is:

.. literalinclude:: ../../../verto/html-templates/blockquote.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Blockquote
***************************************

When overriding the HTML for blockquotes, the following Jinja2 placeholders are available:

- ``{{ content }}`` - The text enclosed by the blockquote tags.
- ``{{ footer }}`` - The provided footer text.
- ``{{ alignment }}`` - The location to add extra CSS classes for alignment.
- ``{{ source }}`` - The URL for the source.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_override_html_template.html
  :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_override_html.md
  :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/blockquote/doc_example_override_html_expected.html
  :language: html
