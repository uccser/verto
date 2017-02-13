Panel
#######################################

**Tag name:** ``panel``

You can include an panel using the following syntax:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage.md
    :language: none

Required Tag Parameters
***************************************

- ``type`` - The type of panel to create.

    - The type is saved as a CCS class (with ``panel-`` prefix) in the panel (this allows colouring of all the same types of panels).

- ``title`` - Text to display as the panel's title.

Optional Tag Parameters
***************************************

- ``subtitle`` - Text to display as the panel's subtitle after the title.
- ``expanded`` - A value to state the panel's state:

    - If given as 'true', the panel contains the CSS class ``panel-expanded`` to state it should be expanded on load.
    - If set to 'always', the panel contains the CSS class ``panel-expanded-always`` to state it should be expanded at load and cannot be closed.
    - When ``expanded`` is not given, the panel contains no extra CSS classes and be closed on load.

The default HTML for a panel is:

.. literalinclude:: ../../../kordac/html-templates/panel.html
   :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage.md
   :language: none

The resulting HTML would be:

.. literalinclude:: ../../../tests/assets/panel/doc_example_basic_usage_expected.html
   :language: html
