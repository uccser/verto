.. _boxed-text:

Boxed Text
#######################################

**Processor name:** ``boxed-text``

You can enclose text inside of a box using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/boxed-text/doc_example_basic_usage.md
   :language: none

Optional Tag Parameters
***************************************

- ``indented`` - If ``yes``, the box will have indentation on the left to match indentation of the first level of a list.

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/boxed-text.html
   :language: css+jinja

Using the example tag above, the resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/boxed-text/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Boxed Text
***************************************

When overriding the HTML for boxed text, the following Jinja2 placeholders are available:

- ``{{ text }}`` - The text enclosed by the boxed text tags.
- ``indented`` - Set to ``yes`` if the indentation parameter was set to ``True``.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/boxed-text/doc_example_override_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/boxed-text/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/boxed-text/doc_example_override_html_expected.html
   :language: html
