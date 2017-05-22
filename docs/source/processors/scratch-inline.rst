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


You can test the output of your Scratch block text at
`scratchblocks.github.io`_.
You can also generate Scratch block text from a published Scratch project at
`scratchblocks.github.io/generator/`_.

.. warning::

    Verto doesn't create the Scratch images, but saves data for another system
    (for example: Django) to create the images.
    See :ref:`accessing-scratch-image-data` section in the scratch documentation.


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

- ``{{ hash }}`` - The hash of the Scratch code-blocks used in the expected filename.

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
.. _scratchblocks.github.io: https://scratchblocks.github.io/#when%20flag%20clicked%0Aclear%0Aforever%0Apen%20down%0Aif%20%3C%3Cmouse%20down%3F%3E%20and%20%3Ctouching%20%5Bmouse-pointer%20v%5D%3F%3E%3E%20then%0Aswitch%20costume%20to%20%5Bbutton%20v%5D%0Aelse%0Aadd%20(x%20position)%20to%20%5Blist%20v%5D%0Aend%0Amove%20(foo)%20steps%0Aturn%20ccw%20(9)%20degrees
.. _scratchblocks.github.io/generator/: https://scratchblocks.github.io/generator/
.. _scratchblocks: https://github.com/scratchblocks/scratchblocks
