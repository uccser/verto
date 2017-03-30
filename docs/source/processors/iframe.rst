Embed iframe
#######################################

**Processor name:** ``iframe``

You can embed a link within an ``iframe`` using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``link`` - The URL to embed within the ``iframe`` element.

The default HTML for iframe is:

.. literalinclude:: ../../../verto/html-templates/iframe.html
    :language: css+jinja

**Example**

Using the following tag:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_basic_usage_expected.html
    :language: html

Overriding HTML for Emedding iframes
***************************************

When overriding the HTML for iframes, the following Jinja2 placeholders are available:

- ``{{ link }}`` - The URL to embed within the ``iframe`` element.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/iframe/doc_example_override_html_expected.html
    :language: html
