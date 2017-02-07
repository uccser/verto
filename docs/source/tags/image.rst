Image
#######################################

You can include an image using the following syntax:

.. code-block:: none

    {image filename="http://placehold.it/350x150"}

Required Tag Parameters
***************************************

- ``filename`` - The path to the image.

    - **Note:** If the given link is a relative (a link that doesn't start with ``http:``), the link will be rendered within a Django static command. For example, the link ``images/example.png`` would be rendered as ``{% static 'images/example.png' %}``.

Optional Tag Parameters
***************************************

- ``alt`` - Description text of the image used when an image is not displayed, or can be read when using a screen reader (for those with reading difficulties).
- ``caption`` - Lists the given text as a caption under the image.
- ``caption-link`` (requires caption parameter) - Converts the caption text into a link to the given caption link URL.
- ``source`` (optional) - Adds the text 'Source' under the image with a link to the given source URL. Displays after the caption if a caption is given.
- ``alignment`` - Valid values are 'left', 'center', or 'right'. Providing one of these values Will add CSS classes to the image for alignment.
- ``hover-text`` - Additional text to be displayed when the user hovers their cursor over the image (note this won't appear on touch devices so use sparingly).

The default HTML for button links is:

.. literalinclude:: ../../../kordac/html-templates/image.html
   :language: css+jinja

Using the following example tag:

.. code-block:: none

    {image filename="http://placehold.it/350x150" caption="Placeholder image" source="https://placehold.it/" title="This is hover text" alignment="left"}

The resulting HTML would be:

.. code-block:: html

    <div>
      <img src="http://placehold.it/350x150" title="This is hover text" class="float-left"/>
      <p>Placeholder image</p>
      <p><a href="https://placehold.it/">Source</a></p>
    </div>

Overriding HTML for Images
***************************************

When overriding the HTML for images, the following Jinja2 placeholders are available:

- ``{{ filename }}`` - The location for the path to the URL.
- ``{{ alt }}`` - The alternative text for the image.
- ``{{ hover_text }}`` - The text to display when the user hovers over the image (see `image title attribute <https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title>`_).
- ``{{ alignment }}`` - The location to add extra CSS classes for alignment.
- ``{{ caption }}`` - The text for the image caption.
- ``{{ caption_link }}`` - The URL for the caption link .
- ``{{ source_link }}`` - The URL for the source .

**Example**

For example, providing the following HTML:

.. code-block:: html

    <div class="text-center">
      <img src="{{ filename }}" class="rounded img-thumbnail">
    </div>

with the following tag:

.. code-block:: none

    {image filename="http://placehold.it/350x150" caption="Placeholder image" source="https://placehold.it/"}

would result in:

.. code-block:: html

    <div class="text-center">
      <img src="http://placehold.it/350x150" class="rounded img-thumbnail">
    </div>
