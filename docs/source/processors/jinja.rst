.. _jinja:

Jinja
#######################################

**Processor name:** ``jinja``

The ``jinja`` processor is a post-processor ensures that Jinja2/Django statements (i.e. ``{% ... %}``) are not escaped like the html of the output document. This allows for further content specific processing after the Verto conversion.

This processor will change the following html:

.. code-block:: html+jinja

  <body>
  {% if thing &lt;= object %}
    <p>
     Something about the &lt;= operation.
    </p>
  {% endif %}
  </body>

By unescaping Jinja2 statements into:

.. code-block:: html+jinja

  <body>
  {% if thing <= object %}
    <p>
     Something about the &lt;= operation.
    </p>
  {% endif %}
  </body>
