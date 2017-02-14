Save Title
#######################################

**Tag name:** ``save-title``

This preprocessor runs before any conversion of Markdown and searches for the first heading in the provided Markdown text.
Once it finds a heading, it saves the text for that heading in the ``title`` attribute of the ``KordacResult`` object.

**Example**

With the following text saved in ``example_string``:

.. literalinclude:: ../../../tests/assets/save-title/doc_example_basic_usage.md
    :language: none

.. code-block:: python

    import kordac
    converter = kordac.Kordac()
    result = converter.convert(example_string)
    print(result.title)

would result in:

.. literalinclude:: ../../../tests/assets/save-title/doc_example_basic_usage_expected.html
    :language: none
