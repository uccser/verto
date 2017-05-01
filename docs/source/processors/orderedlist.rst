.. _orderedlist:

Ordered List (OListProcessor)
#######################################

**Processor name:** ``olist``

This processor overwrites functionality provided by the Python `Markdown <https://pypi.python.org/pypi/Markdown>`_ package allowing for the use of container tags such as :doc:`panel` and :doc:`boxed-text` tags within an ordered list while also providing the same features of the sane lists extension.

Indentation is important when creating ordered lists and is expected to be by default ``4`` spaces for inner content and ``2`` spaces after the number. Authors should follow the following example where indentation spaces are replaced with the ``•`` character.

.. code-block:: none

  1.••Text here.
  ••••More text here.

  2.••Text here.

  ••••1.••List within a list.
  ••••••••More text here.

Sane Lists
*******************************

The Sane Lists extension alters the markdown lists such that types are not allowed to mix. This extension is implemented in Verto by default and therefore does not need to be added as an extension. This means the following markdown:

.. code-block:: none

  1.  Ordered list item.
  *   Not a separate item.

produces the output:

.. code-block:: html

  <ol>
    <li>
      Ordered list item.
  *   Not a separate item.
    </li>
  </ol>
