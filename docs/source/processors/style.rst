.. _style:

Style
#######################################

**Processor name:** ``style``

The ``style`` processor is a pre-processor that checks that the input Markdown to enforce style rules. These rules include:

  - Processor tags have empty lines before and after.
  - Processor tags do not share a line with other text.

An example of a valid document follows:

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_valid.md
   :language: none

Error Example(s)
**************************************

.. note::

  The examples covered in this section are invalid and will raise errors.

The following examples raise errors because the processor tags do not have empty lines before and after.

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_whitespace.md
   :language: none

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_whitespace_1.md
  :language: none

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_whitespace_2.md
   :language: none

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_whitespace_3.md
  :language: none

The following examples raise errors because the processor tags share a line with other text.

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_solitary.md
  :language: none

.. literalinclude:: ../../../verto/tests/assets/style/doc_example_block_solitary_1.md
  :language: none
