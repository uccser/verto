.. _scratch-compatibility:

Scratch Compatibility
#######################################

**Processor name:** ``scratch-compatibility``

The ``scratch-compatibility`` processor is a pre-processor that is enabled by the :doc:`scratch` processor when the ``codehilite`` and ``fenced_code`` extensions are enabled.

When both ``codehilite`` and ``fenced_code`` extensions are enabled the ``fenced_code`` extension modifies the fenced code-blocks by using methods from the ``codehilite`` extension before stashing them to be place in later in the document. The ``scratch-compatibility`` processor is therefore needed to stash the fenced code-blocks before ``fenced_code`` so that they can be processed properly by the :doc:`scratch` processor later.

.. note::

    We consider the ``codehilite`` and ``fenced_code`` extensions a bad way of writing extensions as the output of one dramatically changes depending on if the other is active.

    We believe that an extension like these should produce predictable output and handle compatibility through inputs.

For example if the following markdown document is processed using both the ``codehilite`` and ``fenced_code`` extensions

.. literalinclude:: ../../../verto/tests/assets/scratch/example_multiple_codeblocks_2.md
   :language: none

Verto will produce the following output (which is the same as the ``scratch`` processor would expect):

.. literalinclude:: ../../../verto/tests/assets/scratch/example_multiple_codeblocks_expected_2.html
  :language: html
