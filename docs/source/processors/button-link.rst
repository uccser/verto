Button Link
#######################################

**Processor name:** ``button-link``

You can create a link on a button using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_basic_usage.md
   :language: none

Required Tag Parameters
***************************************

- ``link`` - The URL to link to. *Note: If the given link is a relative, a placeholder for Django to prepend the root is outputted.*
- ``text`` - Text to display on the button.

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/button-link.html
   :language: css+jinja

Using the example tag above, the resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/button-link/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Button Link
***************************************

When overriding the HTML for button links, the following Jinja2 placeholders are available:

- ``{{ link }}`` - The URL.
- ``{{ text }}`` - Text to display on the button.

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
