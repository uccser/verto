Conditional
#######################################

**Processor name:** ``conditional``

You can include an conditional using the following text tag:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_basic_usage.md
   :language: none

.. note::

  Conditional blocks require an understanding of Python logical operators and expressions to function properly. The use of this tag requires co-ordination between authors and developers, as the variables used in the condition are expected when the result is rendered in a template engine.

Tag Parameters
***************************************

Conditional tags function slightly differently to other block text tags. The first conditional text tag must contain the ``if`` flag, followed by optional conditional text tags containing the ``elif`` flag, followed by the optional text tag containing the ``else`` flag.

.. note::

  Any strings within your Python expression need to be wrapped with single quotes (``'``) or escaped double quotes (``\"``).

  Examples:

  .. code-block:: python

    {conditional if="version == 'teacher'"}
    {conditional if="version == \"teacher\""}

To create a set of conditional text tags, follow the following steps:

1. First if block

  - Contains ``if`` flag - Specifies that the conditonal is an opening if statement.
  - Contains ``condition`` parameter - A Python expression to evaluate if true. If true, the enclosed content will be displayed.

2. Then optional else if blocks. Multiple of these blocks can be listed after one another.

  - Contains ``elif`` flag - Specifies that the conditonal is an *else if* following an opening if statement.
  - Contains ``condition`` parameter - A Python expression to evaluate if true. If true, the enclosed content will be displayed.

3. Then optional else block

  - Contains ``else`` flag - Specifies that the conditional is an *else* following an opening if statement, and optional elif statements.

4. Lastly conditional end block

Here is a more complicated example:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_complex_usage.md
   :language: none

**Example**

The default HTML for a conditional is:

.. literalinclude:: ../../../verto/html-templates/conditional.html
  :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_basic_usage.md
  :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_basic_usage_expected.html
  :language: html

Overriding HTML for Conditional
***************************************

When overriding the HTML for conditionals, the following Jinja2 placeholders are available:

- ``{{ if_expression }}`` - The expression from the conditional argument.
- ``{{ if_content }}`` - The content contained within the if expression.
- ``{{ elifs }}`` - An ordered dicitionary of *elif* expressions to content.
- ``{{ has_else }}`` - Whether an else was used in the full if statement.
- ``{{ else_content }}`` - The expression from the conditional argument.

**Example**

For example, if you wanted to output a mako template you would providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/conditional/doc_example_override_html_expected.html
    :language: html
