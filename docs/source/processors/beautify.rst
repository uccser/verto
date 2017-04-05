.. _beautify:

Beautify
#######################################

**Processor name:** ``beautify``

The ``beautify`` processor is a post-processor that tidies and prettifies the output html. The processor works by applying the prettify function from the ``beautifulsoup4`` library just before the final output, this means HTML elements will be separated onto individual lines where children are indented by one space. For example given the follow document:

.. literalinclude:: ../../../verto/tests/assets/beautify/doc_example_basic_usage.md
   :language: none

Verto will prettify it into:

.. literalinclude:: ../../../verto/tests/assets/beautify/doc_example_basic_usage_expected.html
  :language: html

Exception(s)
***************************************

To
For example given the following markdown:

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code.md
   :language: none

Verto will not beautify the code element, producing the output:

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code_expected.html
  :language: html
