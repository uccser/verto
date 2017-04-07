.. _beautify:

Beautify
#######################################

**Processor name:** ``beautify``

The ``beautify`` processor is a post-processor that tidies and prettifies the HTML to give consistent and predictable output. The processor works by applying the prettify function from the ``beautifulsoup4`` library just before the final output, this means HTML elements will be separated onto individual lines where children are indented by one space. For example given the following document:

.. literalinclude:: ../../../verto/tests/assets/beautify/doc_example_basic_usage.md
  :language: none

Verto will prettify it into:

.. literalinclude:: ../../../verto/tests/assets/beautify/doc_example_basic_usage_expected.html
  :language: html

Special Case(s)
***************************************

For example given the following Markdown:

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code.md
  :language: none

Verto with ``beautify`` enabled will produce the following html:

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code_expected.html
  :language: html

Where the ``code`` tag and its contents are unchanged to preserve formatting, this is especially important for whitespace dependent languages.
