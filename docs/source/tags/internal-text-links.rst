Internal Text Links
#######################################

**Tag name:** ``internal-text-links``

This processor will find any internal text links (a link that doesn't start with ``http:``), and prepend the link with a Django template placeholder.
When the resulting HTML is rendered with Django, the Django system can insert the root URL into the template placeholder for correct rendering.

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/internal-text-link.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../tests/assets/internal-text-link/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../tests/assets/internal-text-link/doc_example_basic_usage_expected.html
   :language: html
