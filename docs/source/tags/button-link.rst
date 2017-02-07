Button Link
#######################################

You can create a link on a button using the following syntax:

.. code-block:: none

    {button-link link="http://www.google.com" text="Visit Google"}

Tag Parameters
***************************************

- ``link`` - The URL to link to. *Note: If the given link is a relative, a placeholder for Django to prepend the root is outputted.*
- ``text`` - Text to display on the button.

The default HTML for button links is:

.. code-block:: html

    <a class='button' href='{{ link }}'>{{ text }}</a>

Using the example tag above, the resulting HTML would be:

.. code-block:: html

    <a class='button' href='http://www.google.com'>Visit Google</a>

Overriding HTML for Button Link
***************************************

When overriding the HTML for button links, the following Jinja2 placeholders are available:

- ``{{ link }}`` - The URL.
- ``{{ text }}`` - Text to display on the button.

**Example**

For example, providing the following HTML:

.. code-block:: html

    <a class="btn btn-primary" href="{{ link }}">{{ text }}</a>

with the following tag:

.. code-block:: none

    {button-link link="https://github.com/uccser/kordac" text="Kordac on GitHub"}

would result in:

.. code-block:: html

    <a class="btn btn-primary" href="https://github.com/uccser/kordac">Kordac on GitHub</a>
