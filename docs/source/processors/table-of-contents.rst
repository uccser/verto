Table of Contents
#######################################

**Processor name:** ``table-of-contents``

You can create a placeholder for a web framework (for example: Django) to
insert a table of contents by using the following tag:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_basic_usage.md
    :language: none

Tag Parameters
***************************************

There are no required or optional tag parameters for table of contents.

**Example**

Using the following tag:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_basic_usage_expected.html
    :language: html

Overriding HTML for Table of Contents
***************************************

There are no Jinja2 placeholders available when overriding the HTML for table
of contents.

The default HTML for table of contents is:

.. literalinclude:: ../../../verto/html-templates/table-of-contents.html
   :language: css+jinja

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/table-of-contents/doc_example_override_html_expected.html
    :language: html
