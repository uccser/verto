Using Verto
#######################################

.. currentmodule:: Verto

Using Verto to convert Markdown is a process of:

1. Importing the installed Verto package.
2. Creating a Verto converter.
3. Passing Markdown text through the Verto ``convert`` method and saving the result object.
4. Accessing data from the result object.

Step 1: Importing Verto
=======================================

If Verto has been installed correctly, importing the package can be completed by:

.. code-block:: python

  import verto


Step 2: Creating Verto converter
=======================================

Once the module is imported, you can create a Verto converter creating an Verto object:

.. code-block:: python

  converter = verto.Verto()

``Verto()`` has optional parameters to customise the converter. These are:

- ``processors`` - A set of processor names given as strings for the converter to use. If this parameter is not given, the default processors are used. If ``processors`` is provided, all processors not listed are skipped.

  - *For example:* Creating a Verto converter that only deletes comment tags would be done by the following command:

    .. code-block:: python

      converter = verto.Verto(processors={"comment"})

- ``html_templates`` - A dictionary of HTML templates to override existing HTML templates for processors. The dictionary contains processor names given as a string as keys mapping HTML strings as values.

  The documentation page for each processor specificies how to create custom HTML for that processor.

  - *For example:* Creating a Verto converter that uses  ``<img src={{ source }}>`` as custom HTML for ``image`` tags would be done by the following command:

    .. code-block:: python

      converter = verto.Verto(html_templates={'image': '<img src={{ source }}>'})

- ``extensions`` -  A list of extra Markdown extensions to run in the converter. Details on how to use this parameter can be found on the :doc:`extensions` page.

- ``settings`` - A dictionary of settings to override default Verto settings. The following settings are available:

  - ``ADD_DEFAULT_INTERACTIVE_THUMBNAILS_TO_REQUIRED_FILES`` - Boolean stating whether default interactive thumbnail filepaths should be added to the required files set of images. Default is ``True``.

  - ``ADD_CUSTOM_INTERACTIVE_THUMBNAILS_TO_REQUIRED_FILES`` - Boolean stating whether custom interactive thumbnail filepaths provided as tag arguments should be added to the required files set of images. External images are never added. Default is ``True``.

  - ``PROCESSOR_ARGUMENT_OVERRIDES`` - A dictionary to modify the default argument rules for each tag. The default rules can found by reading the documentation for each tag.

    - *For example:* By default, the ``image-inline`` tag requires alt text to be given, to change this, the following custom argument rules would be used:

      .. code-block:: python

        {
          "image-inline": {
            "alt": False
          }
        }

  .. warning::

    Some tags have multiple processors behind them (for example, the ``image-inline``, ``image-container`` and ``image-tag`` processors are all used for images).
    This means that if you would like to change the default rules of one or more of their arguments, this will need to be done for each of the processors
    individually. For example, to set the ``alt`` argument as ``False`` for all images, the custom argument rules would look as follows:

    .. code-block:: python

        {
          "image-inline": {
            "alt": False
          },
          "image-tag": {
            "alt": False
          },
          "image-container": {
            "alt": False
          }
        }


Step 3: Convert Markdown with converter
=======================================

To convert Markdown to HTML with a Verto converter, we call the ``convert()`` method. The method returns a ``VertoResult`` object.

.. code-block:: python

  text = """
  This **is** a line of Markdown.

  {comment This is a comment using a Verto tag}

  This is a *different* line of Markdown.
  """
  result = converter.convert(text)

.. _accessing_verto_data:

Step 4: Accessing VertoResult data
=======================================

The ``VertoResult`` object contains several attributes which can be accessed using the dot notation. Continuing from our previous example, the following command would print the converted HTML.

.. code-block:: python

  print(result.html_string)

The following attributes are available:

- ``html_string`` - A resulting string of HTML after conversion by Verto.
- ``title`` - The text of the first heading saved by the ``save-title`` processor.
- ``required_files`` - A dictionary of files encountered in a Verto conversion. The dictionary has a string for the file type as the key (for example: ``image``) and a set of all file paths encountered as the value (for example: ``{'image/face.png', 'image/logo.png`}``).

  - See :ref:`accessing-scratch-image-data` for data from Scratch processor.

- ``heading_tree`` - A tuple of namedtuples which describes the tree of headings, as generated by our heading processor. Each namedtuple contains a ``title`` (string), ``title_slug`` (string), ``level`` (integer) and ``children`` (tuple of nodes).

  - For example the heading root after a conversion of a file:

    .. code-block:: python

      (
        HeadingNode(title='This is an H1', title_slug='this-is-an-h1', level=1, children=(
          HeadingNode(title='H2 Title', title_slug='h2-title', level=2, children=())
        )),
        HeadingNode(title='This is an H1', title_slug='this-is-an-h11', level=1, children=()),
      )

- ``required-glossary-terms`` - A dictionary of term slugs to a list of tuples containing reference text and link IDs.

  - Here is an example of the ``required-glossary-terms`` after a conversion of a file:

    .. code-block:: python

      required-glossary-terms = {
        "algorithm":
          [("Binary Search", "glossary-algorithm"),
           ("Quick Sort", "glossary-algorithm-2"),
           ("Merge Sort", "glossary-algorithm-3")],
        "alphabet":
          [("Formal Languages", "glossary-alphabet")],
        "brooks-law":
          []
      }

(Optional) Step 5: Clearing Saved Data
=======================================

Lastly there is some data that is saved between conversions such as ``required_files`` and unique ids used in the ``glossary`` and for ``headings``. This can be cleared by using the following method:

  .. code-block:: python

    converter.clear_saved_data()

Configuring Verto converter after creation
===============================================

The following functions allow you to change the processors or HTML templates used in conversion by the Verto converter after its creation.

Changing processors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: verto.Verto.update_processors(processors)

.. automethod:: verto.Verto.processor_defaults(processors)

  This function is useful if you want to make minor changes to the default used processors. For example: You wish to still use all default processors but skip video tags:

  .. code-block:: python

    processors = Verto.processor_defaults()
    processors.remove('video')
    converter = Verto(processors=processors)

  Or with an existing Verto instance ``converter``:

  .. code-block:: python

    processors = Verto.processor_defaults()
    processors.remove('video')
    converter.update_processors(processors)

Changing HTML templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: verto.Verto.update_templates(html_templates)

.. automethod:: verto.Verto.clear_templates()

Full list of package methods
=======================================

.. autoclass:: verto.Verto()
  :members: __init__, convert, update_processors, processor_defaults, update_templates, clear_templates, clear_saved_data

.. autoclass:: verto.Verto.VertoResult()

  .. attribute:: html_string

    The converted HTML as a string.

  .. attribute:: title

    The text of the first heading found by the :doc:`processors/save-title` processor.

  .. attribute:: required_files

    A dictionary of files encountered in a Verto conversion. The dictionary has a string for the file type as the key (for example: ``image``) and a set of all file paths encountered as the value (for example: ``{'image/face.png', 'image/logo.png`}``).

  .. attribute:: heading_tree

     A tuple of namedtuples which describes the tree of headings, as generated by our heading processor. Each namedtuple contains a title (string), title_slug (string), level (integer) and children (tuple of nodes).

  .. attribute:: required_glossary_terms

     A dictionary of terms to a list of tuples containing reference text and link IDs.
