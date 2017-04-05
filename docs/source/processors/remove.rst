.. _remove:

Remove
#######################################

**Processor name:** ``remove``

The ``remove`` processor is a post-processor that searches the document for remove html-elements (i.e. ``<remove>...</remove>``) and removes them from the document leaving the content unchanged. This is useful when creating html-templates as they can be used to add multiple siblings to a parent element that are not valid html, allowing the document to be parsed as a valid html-document up until their removal.

.. note::

    The ``remove`` processor does not remove the content between the remove element tags, but instead only removes the tag itself. 

For example the :doc:`conditional` processors default html template, as follows, does not produce valid html and so is placed within a remove element so that Verto can add it to the element tree.

.. literalinclude:: ../../../verto/html-templates/conditional.html
   :language: html+jinja

Therefore a markdown document like:

.. literalinclude:: ../../../verto/tests/assets/remove/doc_example_basic_usage.md
   :language: html+jinja

When parsed with Verto will produce the output:

.. literalinclude:: ../../../verto/tests/assets/remove/doc_example_basic_usage_expected.html
  :language: html+jinja
