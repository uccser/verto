Scratch (Inline)
#######################################

**Processor name:** ``scratch-inline``

.. note::

  The inline scratch processor works similarly to the default :doc:`scratch` processor except that it matches inline codeblocks instead and requires a colon after the scratch tag.

.. danger::

  Scratch blocks require an understanding of the Scratch programming language and how Verto is integrated with other systems. The use of this processor requires co-ordination between authors and developers to achieve the desired functionality.

.. note::

    The following examples assume usage of the fenced code extension, by having
    ``markdown.extensions.fenced_code`` in the list of extensions given to Verto.

You can include an image of Scratch blocks using
`Scratch Block Plugin notation`_ using the following notation:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_basic_usage.md
    :language: none

to produce the following image with the ``scratch:`` stripped:

.. image:: ../images/scratch_inline_example.png

which is inserted between the paragraph text.

You can test the output of your Scratch block text (and create PNG
or SVG images) at `scratchblocks.github.io`_.

.. warning::

    Verto doesn't create the Scratch images itself, but prepares it for a
    JavaScript library to render these in the user's browser.
    See :ref:`rendering-scratch-images` section below.

The default HTML for scratch blocks is:

.. literalinclude:: ../../../verto/html-templates/scratch-inline.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_basic_usage_expected.html
    :language: html


Overriding HTML for Scratch
***************************************

When overriding the HTML for Scratch code, the following Jinja2 placeholders are available:

- ``{{ scratch_block }}`` - The text of the Scratch blocks notation.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../verto/tests/assets/scratch-inline/doc_example_override_html_expected.html
    :language: html

.. _Scratch Block Plugin notation: https://wiki.scratch.mit.edu/wiki/Block_Plugin
.. _scratchblocks.github.io: https://scratchblocks.github.io/#?style=scratch3&script=say%20%5Bhi%5D%20for%20(2)%20secs
