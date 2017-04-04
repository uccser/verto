.. _beautify:

Beautify
#######################################

**Processor name:** ``beautify``

The ``beautify`` processor is a post-processor in Verto that gives us consistent and predictable output. To achieve this goal the output of the Verto is run through the ``beautifulsoup4`` prettify function, where each HTML is on its own line and children are indented one space in.

This means that html like:

.. code-block:: html

  <body>
  <h1>Example Heading</h1>
  <p>Example paragraph.</p>
  <div><p>Example paragraph within a div.</p></div>
  </body>

Becomes:

.. code-block:: html

  <body>
   <h1>
    Example Heading
   </h1>
   <p>
    Example paragraph.
   </p>
   <div>
    <p>
     Example paragraph within a div.
    </p>
   </div>
  </body>

Special Case(s)
**************************************

Given the following markdown:

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code.md
  :language: none

Verto with ``beautify`` enabled will produce the following html, Where the ``code`` tag and its contents are unchanged to preserve formatting, this is especially important for whitespace dependent languages.

.. literalinclude:: ../../../verto/tests/assets/beautify/example_inline_code_expected.html
  :language: html
