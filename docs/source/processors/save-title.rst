Save Title
#######################################

**Tag name:** ``save-title``

This preprocessor runs before any conversion of Markdown and searches for a heading in the first line of provided Markdown text.
If a heading is found on the first line, it saves the text for that heading in the ``title`` attribute of the ``VertoResult`` object.

**Example**

With the following text saved in ``example_string``:

.. literalinclude:: ../../../verto/tests/assets/save-title/doc_example_basic_usage.md
    :language: none

.. code-block:: python

    import verto
    converter = verto.Verto()
    result = converter.convert(example_string)
    print(result.title)

would result in:

.. literalinclude:: ../../../verto/tests/assets/save-title/doc_example_basic_usage_expected.html
    :language: none
