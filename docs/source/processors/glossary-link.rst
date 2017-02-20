Glossary Link
#######################################

**Processor name:** ``glossary-link``

You can include a link to a glossary term using the following text tag:

.. literalinclude:: ../../../kordac/tests/assets/glossary-link/doc_example_basic_usage.md
    :language: none

.. note::

    The ``glossary-link`` tag is an inline tag.

Required Tag Parameters
***************************************

- ``term`` - The slug of the term to link to in the glossary (for example ``binary-search``).

    - Each term encountered is added to the required glossary terms stored by Kordac. The set of terms can be accessed after conversion, see :ref:`accessing_kordac_data`.
    - When using the default HTML template, the term is stored in a `data attribute`_ named ``data-glossary-term``.

Optional Tag Parameters
***************************************

- ``reference-text`` - If included, adds a back reference link using the given the text after the definition.

    - If back reference text is included, then an ID should be generated for the link. Currently the ID is generated as ``glossary-`` + the term slug. If successive back links for the same term are found then an incrementing number is appended to the generated ID.

      The back reference text and ID are stored in the required glossary terms, and can be accessed after conversion, see :ref:`accessing_kordac_data`.

      .. warning::

        The IDs generated assume no other Kordac generated HTML is included on the same page. If two (or more) separate conversions of Markdown by Kordac are displayed on the same page, there may be ID conflicts.

.. note::

    The text between the start and end tags is used as text to display as a link to the glossary definition. If no text is given, then the link is invisible and can be used to add a back reference to be particular point.

The default HTML for glossary links is:

.. literalinclude:: ../../../kordac/html-templates/glossary-link.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/glossary-link/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/glossary-link/doc_example_basic_usage_expected.html
    :language: html

.. _data attribute: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*
