.. _unorderedlist:

Unordered List (UListProcessor)
#######################################

**Processor name:** ``ulist``

This processor overwrites functionality provided by the Python `Markdown <https://pypi.python.org/pypi/Markdown>`_ package allowing for the use of container tags such as :doc:`panel` and :doc:`boxed-text` tags within an unordered list while also providing the same features of the sane lists extension.

Indentation is important when creating unordered lists and is expected to be ``4`` spaces by default for inner content and ``3`` spaces after the bullet. Authors should follow the following example where indentation spaces are replaced with the ``•`` character.

.. code-block:: none

  *•••Text here.
  ••••More text here.

  *•••Text here.

  ••••*•••List within a list.
  ••••••••More text here.

See :doc:`orderedlist` for details on Sane Lists.
