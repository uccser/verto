Internal Link
#######################################

**Processor name:** ``internal-link``

This processor will find any internal links (a link that doesn't start with ``http:``), and prepend the link with a Django template placeholder.
When the resulting HTML is rendered with Django, the Django system can insert the root URL into the template placeholder for correct rendering.

The default HTML for internal links is:

.. literalinclude:: ../../../kordac/html-templates/internal-link.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/internal-link/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/internal-link/doc_example_basic_usage_expected.html
   :language: html

Overriding HTML for Internal Links
***************************************

When overriding the HTML for internal links, the following Jinja2 placeholders are available:

- ``{{ link_path }}`` - The given link URL.

**Example**

For this example, we wish to create HTML to be used in a static site system (not Django). The internal link processor should append the website's URL to each link.

For example, providing the following HTML template:

.. literalinclude:: ../../../kordac/tests/assets/internal-link/doc_example_override_html_template.html
  :language: css+jinja

with the following Markdown:

.. literalinclude:: ../../../kordac/tests/assets/internal-link/doc_example_override_html.md
  :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/internal-link/doc_example_override_html_expected.html
  :language: html
