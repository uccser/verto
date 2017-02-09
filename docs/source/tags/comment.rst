Comment
#######################################

**Tag name:** ``comment``

You can include comments in the source text that are deleted before conversion:

.. literalinclude:: ../../../kordac/tests/assets/comment/doc_example_basic_usage.md
   :language: none

Comment tags have no parameters or HTML templates associated with them.

**Example**

The following text:

.. literalinclude:: ../../../kordac/tests/assets/comment/doc_example_multiple_usage.md
   :language: none

would result in (after Kordac has finished conversion):

.. literalinclude:: ../../../kordac/tests/assets/comment/doc_example_multiple_usage_expected.html
   :language: html
