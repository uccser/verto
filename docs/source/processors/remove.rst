.. _remove:

Remove
#######################################

**Processor name:** ``remove``

The ``remove`` processor is a post-processor in Verto that allows for the creation of html that would not otherwise be possible by allowing for the use of a remove html tag (``<remove>...</remove>``) during processing, which is removed just before output.

The main use of the ``remove`` processor is for developers to create invalid html-templates to be formatted into the the html tree. For example this tag is useful for things like conditionals that need to place a combination of text and elements in the parent node while also remaining customisable and consistent with the overriding of other processors. When this processor is run only the tag is removed not the content, this means that html like:

.. code-block:: html

  <body>
   <h1>Example Heading</h1>
   <p>Example paragraph.</p>
   <div>
    <remove>
     <p>Example paragraph within a div.</p>
    </remove>
   </div>
  </body>

Becomes:

.. code-block:: html

  <body>
   <h1>Example Heading</h1>
   <p>Example paragraph.</p>
   <div>
    <p>Example paragraph within a div.</p>
   </div>
  </body>
