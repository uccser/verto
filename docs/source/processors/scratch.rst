Scratch
#######################################

**Processor name:** ``scratch``

You can include an image of Scratch blocks using
`Scratch Block Plugin notation`_ using the following notation:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_basic_usage.md
    :language: none

to produce the following image:

.. image:: ../images/scratch_blocks_example.png

The syntax is the same for default Markdown code blocks, but Kordac handles the
content differently due to the ``scratch`` language set at the start.

You can test the output of your Scratch block text at
`scratchblocks.github.io`_.

.. warning::

    Kordac doesn't create the Scratch images, but saves data for another system
    (for example: Django) to create the images.
    See :ref:`accessing-scratch-image-data` section below.

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/scratch.html
    :language: css+jinja

Using the following example tag:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_basic_usage.md
    :language: none

The resulting HTML would be:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_basic_usage_expected.html
    :language: html

.. _accessing-scratch-image-data:

Accessing Scratch image data
***************************************

When Kordac encounters a code block with the Scratch language (see example
above), it doesn't not generate the image but saves the enclosed text and hash
of the text in the ``required_files`` attribute under the key
``scratch_images``.

Here is an example of the result of required files after the parsing two
Scratch blocks:

.. code-block:: python

    required_files = {
        "scratch_images": [
            {
            "text": "when flag clicked\nsay [Hi]\n",
            "hash": "12203e8a9d57d5a3bdc384522acd150c"
            },
            {
              "text": "when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees\n",
              "hash": "51b6c618e8440f64869ee24ad8405930"
            }
        ]
    }

The processor replaces the text with an image linked to the expected location
of the image.

After Kordac has completed a conversion, you will need to retrieve this data
from ``required_files`` and render it to an image in the expected location.
The `scratchblocks`_ renderer on GitHub allows of rendering to an SVG or PNG.

Overriding HTML for Scratch
***************************************

When overriding the HTML for Scratch code, the following Jinja2 placeholders are available:

- ``{{ hash }}`` - The hash of the Scratch code used in the expected filename.

**Example**

For example, providing the following HTML:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_override_html_template.html
    :language: css+jinja

with the following tag:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_override_html.md
    :language: none

would result in:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_override_html_expected.html
    :language: html

.. _Scratch Block Plugin notation: https://wiki.scratch.mit.edu/wiki/Block_Plugin
.. _scratchblocks.github.io: https://scratchblocks.github.io/#when%20flag%20clicked%0Aclear%0Aforever%0Apen%20down%0Aif%20%3C%3Cmouse%20down%3F%3E%20and%20%3Ctouching%20%5Bmouse-pointer%20v%5D%3F%3E%3E%20then%0Aswitch%20costume%20to%20%5Bbutton%20v%5D%0Aelse%0Aadd%20(x%20position)%20to%20%5Blist%20v%5D%0Aend%0Amove%20(foo)%20steps%0Aturn%20ccw%20(9)%20degrees
.. _scratchblocks: https://github.com/scratchblocks/scratchblocks