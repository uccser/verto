Scratch
#######################################

.. note::

    The following examples assume usage of the fenced code extension, by having
    ``markdown.extensions.fenced_code`` in the list of extensions given to Kordac.

**Processor name:** ``scratch``

You can include an image of Scratch blocks using
`Scratch Block Plugin notation`_ using the following notation:

.. literalinclude:: ../../../kordac/tests/assets/scratch/doc_example_basic_usage.md
    :language: none

to produce the following image:

.. image:: ../images/scratch_blocks_example.png

The syntax is the same for default Markdown code blocks. The only difference
is that Kordac handles the content differently due to the ``scratch`` language
set at the start.

.. note::

    This processor also works with syntax introduced by the `fenced_blocks`
    and/or `codehilite` extensions.

You can test the output of your Scratch block text at
`scratchblocks.github.io`_.
You can also generate Scratch block text from a published Scratch project at
`scratchblocks.github.io/generator/`_.

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

.. _scratch_options:

Options
***************************************
Options that change the output behaviour can be specified by appending them after the language separated by ``:``. The options avaliable are:

- ``split`` - This option turns separate Scratch blocks (which are dictated by an empty line) into separate images.
- ``random`` - This parameter randomises the order of separate Scratch blocks (which are dictated by an empty line).


For example options can be used like:

.. literalinclude:: ../../../kordac/tests/assets/scratch/example_split_codeblocks.md
    :language: none

Or for more than one option:

.. literalinclude:: ../../../kordac/tests/assets/scratch/example_random_split_codeblocks.md
    :language: none

.. _accessing-scratch-image-data:

Accessing Scratch image data
***************************************

When Kordac encounters a code block with the Scratch language (see example
above), it doesn't not generate the image but saves the enclosed text and hash
of the text in the ``required_files`` attribute under the key
``scratch_images``.

The following is an example of the result of required files after the parsing
two Scratch blocks, where the ``scratch_images`` key points to a set of
``namedtuple`` objects containing a ``hash`` (string) and ``text`` (string):

.. code-block:: python

    required_files = {
        "scratch_images": [
            ScratchImageMetaData(
              hash="a3b77ed3c3fa57e43c830e338dc39d292c7def676e0e8f7545972b7da20275da",
              text="when flag clicked\nsay [Hi]\n"
            ),
            ScratchImageMetaData(
              hash="a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576",
              text="when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees\n"
            )
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

- ``{{ hash }}`` - A list of hashes of the Scratch code-blocks used in the expected filename(s).

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
.. _scratchblocks.github.io/generator/: https://scratchblocks.github.io/generator/
.. _scratchblocks: https://github.com/scratchblocks/scratchblocks
