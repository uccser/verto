Glossary Link
#######################################

**Processor name:** ``glossary-link``

You can include a link to a glossary term using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_basic_usage.md
    :language: none

.. note::

    The ``glossary-link`` tag is an inline tag.

Required Tag Parameters
***************************************

- ``term`` - The slug of the term to link to in the glossary (for example ``binary-search``).

    - Each term encountered is added to the required glossary terms stored by Verto. The set of terms can be accessed after conversion, see :ref:`accessing_verto_data`.
    - When using the default HTML template, the term is stored in a `data attribute`_ named ``data-glossary-term``.

Optional Tag Parameters
***************************************

- ``reference-text`` - If included, adds a back reference link using the given the text after the definition.

    - If back reference text is included, then an ID should be generated for the link. Currently the ID is generated as ``glossary-`` + the term slug. If successive back links for the same term are found then an incrementing number is appended to the generated ID.

      The back reference text and ID are stored in the required glossary terms, and can be accessed after conversion, see :ref:`accessing_verto_data`.

      .. warning::

        The IDs generated assume no other Verto generated HTML is included on the same page. If two (or more) separate conversions of Markdown by Verto are displayed on the same page, there may be ID conflicts.

.. note::

    The text between the start and end tags is used as text to display as a link to the glossary definition. If no text is given, then the link is invisible and can be used to add a back reference to be particular point.

The default HTML for glossary links is:

.. literalinclude:: ../../../verto/html-templates/glossary-link.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_basic_usage_expected.html
    :language: html

Possible Glossary Usage with Django
***************************************

While Verto will generate links for glossary terms from the HTML template, these links will not work by themselves.

The expected usage is to display the links on a webpage and when a user clicks a link, a JavaScript handler will catch the click.
The handler can view the term in the ``data-glossary-term`` attribute and send a request to a database to retrieve the term's definition and associated data.
The handler can then display this information via popup/modal/etc once it recieves the data.

Verto also provides the back reference text and ID for terms in the required glossary terms which can be accessed after conversion (see :ref:`accessing_verto_data`).
This data can be added to the database before the web server is run for displaying to users.

Overriding HTML for Glossary Links
***************************************

When overriding the HTML for glossary links, the following Jinja2 placeholders are available:

- ``{{ term }}`` - The slug of the term to link to.
- ``{{ text }}`` - The text inclosed by ``{glossary-link}`` tags that should be the link to the glossary definition.
- ``{{ id }}`` - The ID of the glossary term's back reference.

**Example**

For example, we wish to create glossary links that link to a static glossary page, where each definition has a header with an ID of the term's slug.

By providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_override_html_template.html
   :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/glossary-link/doc_example_override_html_expected.html
   :language: html

.. _data attribute: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/data-*
