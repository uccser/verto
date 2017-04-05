.. _jinja:

Jinja
#######################################

**Processor name:** ``jinja``

The ``jinja`` processor is a post-processor that is used to undo HTML escaping on Jinja/Django statements (i.e. ``{% ... %}``) that may be present in the document for further processing of the document after conversion. This processor does not do any sanitizing of the Jinja/Django statements and therefore should not be used on untrusted input without sanitation before or after the Verto conversion. This processor  should be used with the :doc:`conditional` as the default html-template produces Jinja statements.

For example the following document with an if statement:

.. literalinclude:: ../../../verto/tests/assets/jinja/doc_example_basic_usage.md
   :language: html+jinja

Verto will unescape the Jinja/Django statement and produce the following output:

.. literalinclude:: ../../../verto/tests/assets/jinja/doc_example_basic_usage_expected.html
  :language: html+jinja
