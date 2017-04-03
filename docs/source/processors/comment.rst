Comment
#######################################

**Processor name:** ``comment``

You can include comments in the source text that are deleted before conversion:

.. literalinclude:: ../../../verto/tests/assets/comment/doc_example_basic_usage.md
   :language: none

Comment tags have no parameters or HTML templates associated with them.

**Example**

The following text:

.. literalinclude:: ../../../verto/tests/assets/comment/doc_example_multiple_usage.md
   :language: none

would result in (after Verto has finished conversion):

.. literalinclude:: ../../../verto/tests/assets/comment/doc_example_multiple_usage_expected.html
   :language: html
