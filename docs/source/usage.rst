Using Kordac
#######################################

.. currentmodule:: Kordac

Using Kordac to convert Markdown is a process of:

1. Importing the installed Kordac package.
2. Creating a Kordac converter.
3. Passing Markdown text through the Kordac ``run`` method and saving the result object.
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

- ``tags`` - A set of tag names given as strings for the converter to use. If this parameter is not given, the default tags are used. If ``tags`` is provided, all processors not listed are skipped.

  - *For example:* Creating a Kordac converter that only deletes comment tags would be done by the following command:

    .. code-block:: python

      converter = kordac.Kordac(tags={"comment"})

- ``html_templates`` - A dictionary of HTML templates to override existing HTML templates for tags. The dictionary contains tag names given as a string as keys mapping HTML strings as values.

  The documentation page for each tag specificies how to create custom HTML for that tag.

  - *For example:* Creating a Kordac converter that uses  ``<img src={{ source }}>`` as custom HTML for ``image`` tags would be done by the following command:

    .. code-block:: python

      converter = kordac.Kordac(html_templates={'image': '<img src={{ source }}>'})

- ``extensions`` -  A list of extra Markdown extensions to run in the converter. Details on how to use this parameter can be found on the :doc:`extensions` page.

Step 3: Convert Markdown with converter
=======================================

To convert Markdown to HTML with a Kordac converter, we call the ``run()`` method. The method returns a ``KordacResult`` object.

.. code-block:: python

  text = """
  This **is** a line of Markdown.

  {comment This is a comment using a Kordac tag}

  This is a *different* line of Markdown.
  """
  result = converter.run(text)

Step 4: Accessing KordacResult data
=======================================

The ``KordacResult`` object contains several attributes which can be accessed using the dot notation. Continuing from our previous example, the following command would print the converted HTML.

.. code-block:: python

  print(result.html_string)

The following attributes are available:

- ``html_string`` - A resulting string of HTML after conversion by Kordac.
- ``title`` - The text of the first heading saved by the ``save-title`` processor.

Configuring Kordac converter after creation
===============================================

The following functions allow you to change the tags or HTML templates used in conversion by the Kordac converter after its creation.

Changing tags
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: kordac.Kordac.update_tags(tags)

.. automethod:: kordac.Kordac.tag_defaults(tags)

  This function is useful if you want to make minor changes to the default used tags. For example: with an existing Kordac converter ``converter``, you wish to still use all default tags but now skip video tags:

  .. code-block:: python

    tags = converter.tag_defaults()
    tags.remove('video')
    converter.update_tags(tags)

Changing HTML templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: kordac.Kordac.update_templates(html_templates)

.. automethod:: kordac.Kordac.default_templates(tags)


Full list of package methods
=======================================



.. autoclass:: kordac.Kordac()
  :members: __init__, run, update_tags, tag_defaults, update_templates, default_templates

.. autoclass:: kordac.Kordac.KordacResult()
