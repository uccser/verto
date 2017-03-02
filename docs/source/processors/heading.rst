Heading
#######################################

**Processor name:** ``heading``

This replaces the output of Markdown headings that begin with the ``#`` character (atx-style headings).
This processor an ID to each heading which allows for linking to a heading, and adds the heading number before the heading text.

.. note::

    This processor replaces the output of the standard markdown block processor for atx-style headings.

You may creating a heading by using the following format:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_basic_usage.md
   :language: none

The default HTML for headings is:

.. literalinclude:: ../../../kordac/html-templates/heading.html
   :language: css+jinja

**Example**

Using the following tag:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_basic_usage_expected.html
   :language: html


Overriding HTML for Heading
***************************************

When overriding the HTML for heading, the following Jinja2 placeholders are available:

 - ``{{ headling_level }}`` - A number representing the heading level.
 - ``{{ heading_type }}`` - The string of the heading tag i.e. *h1* etc.
 - ``{{ title }}`` - The title of the heading.
 - ``{{ title_slug }}`` - A slug of the heading, useful for ids.
 - ``{{ level_1 }}`` - The current first level heading number.
 - ``{{ level_2 }}`` - The current second level heading number.
 - ``{{ level_3 }}`` - The current third level heading number.
 - ``{{ level_4 }}`` - The current fourth level heading number.
 - ``{{ level_5 }}`` - The current fifth level heading number.
 - ``{{ level_6 }}`` - The current sixth level heading number.

The ``level`` parameters are useful for generating levels trails so that users know where they are exactly within the document.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_override_html_template.html
   :language: css+jinja

with the following markdown:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_override_html.md
   :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/heading/doc_example_override_html_expected.html
   :language: html
