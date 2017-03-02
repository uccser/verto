Embed iframe
#######################################

**Processor name:** ``iframe``

You can embed a link within an ``iframe`` using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/iframe/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``link`` - The URL to embed within the ``iframe``.

The default HTML for iframe is:

.. literalinclude:: ../../../kordac/html-templates/iframe.html
    :language: css+jinja

**Example**

Using the following tag:

.. literalinclude:: ../../../kordac/tests/assets/iframe/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/iframe/doc_example_basic_usage_expected.html
    :language: html
