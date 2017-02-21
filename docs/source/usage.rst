Using Kordac
#######################################

.. currentmodule:: Kordac

Using Kordac to convert Markdown is a process of:

1. Importing the installed Kordac package.
2. Creating a Kordac converter.
3. Passing Markdown text through the Kordac ``convert`` method and saving the result object.
4. Accessing data from the result object.

Step 1: Importing Kordac
=======================================

If Kordac has been installed correctly, importing the package can be completed by:

.. code-block:: python

  import kordac


Step 2: Creating Kordac converter
=======================================

Once the module is imported, you can create a Kordac converter creating an Kordac object:

.. code-block:: python

  converter = kordac.Kordac()

``Kordac()`` has optional parameters to customise the converter. These are:

- ``processors`` - A set of processor names given as strings for the converter to use. If this parameter is not given, the default processors are used. If ``processors`` is provided, all processors not listed are skipped.

  - *For example:* Creating a Kordac converter that only deletes comment tags would be done by the following command:

    .. code-block:: python

      converter = kordac.Kordac(processors={"comment"})

- ``html_templates`` - A dictionary of HTML templates to override existing HTML templates for processors. The dictionary contains processor names given as a string as keys mapping HTML strings as values.

  The documentation page for each processor specificies how to create custom HTML for that processor.

  - *For example:* Creating a Kordac converter that uses  ``<img src={{ source }}>`` as custom HTML for ``image`` tags would be done by the following command:

    .. code-block:: python

      converter = kordac.Kordac(html_templates={'image': '<img src={{ source }}>'})

- ``extensions`` -  A list of extra Markdown extensions to run in the converter. Details on how to use this parameter can be found on the :doc:`extensions` page.

Step 3: Convert Markdown with converter
=======================================

To convert Markdown to HTML with a Kordac converter, we call the ``convert()`` method. The method returns a ``KordacResult`` object.

.. code-block:: python

  text = """
  This **is** a line of Markdown.

  {comment This is a comment using a Kordac tag}

  This is a *different* line of Markdown.
  """
  result = converter.convert(text)

.. _accessing_kordac_data:

Step 4: Accessing KordacResult data
=======================================

The ``KordacResult`` object contains several attributes which can be accessed using the dot notation. Continuing from our previous example, the following command would print the converted HTML.

.. code-block:: python

  print(result.html_string)

The following attributes are available:

- ``html_string`` - A resulting string of HTML after conversion by Kordac.
- ``title`` - The text of the first heading saved by the ``save-title`` processor.
- ``required_files`` - A dictionary of files encountered in a Kordac conversion. The dictionary has a string for the file type as the key (for example: ``image``) and a set of all file paths encountered as the value (for example: ``{'image/face.png', 'image/logo.png`}``).

Configuring Kordac converter after creation
===============================================

The following functions allow you to change the processors or HTML templates used in conversion by the Kordac converter after its creation.

Changing processors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: kordac.Kordac.update_processors(processors)

.. automethod:: kordac.Kordac.processor_defaults(processors)

  This function is useful if you want to make minor changes to the default used processors. For example: You wish to still use all default processors but skip video tags:

  .. code-block:: python

    processors = Kordac.processor_defaults()
    processors.remove('video')
    converter = Kordac(processors=processors)

  Or with an existing Kordac instance ``converter``:

  .. code-block:: python

    processors = Kordac.processor_defaults()
    processors.remove('video')
    converter.update_processors(processors)

Changing HTML templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: kordac.Kordac.update_templates(html_templates)

.. automethod:: kordac.Kordac.clear_templates()

Full list of package methods
=======================================

.. autoclass:: kordac.Kordac()
  :members: __init__, convert, update_processors, processor_defaults, update_templates, clear_templates

.. autoclass:: kordac.Kordac.KordacResult()

  .. attribute:: html_string

    The converted HTML as a string.

  .. attribute:: title

    The text of the first heading found by the :doc:`processors/save-title` processor.

  .. attribute:: required_files

    A dictionary of files encountered in a Kordac conversion. The dictionary has a string for the file type as the key (for example: ``image``) and a set of all file paths encountered as the value (for example: ``{'image/face.png', 'image/logo.png`}``).
