Welcome to Kordac
#################

.. warning::

  This repository is currently in development!
  Therefore features may not be implemented yet, may change, be buggy, or completely broken.

Kordac is an extension of the Python `Markdown <https://pypi.python.org/pypi/Markdown>`_ package, which allows authors to include complex HTML elements with simple text tags in their Markdown files.

For example:

.. code-block:: python

    >>> import kordac
    >>> converter = kordac.Kordac()
    >>> result = converter.run('{video url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"}')
    >>> result.html_string
    "<iframe src='http://www.youtube.com/embed/dQw4w9WgXcQ?rel=0' frameborder='0' allowfullscreen></iframe>"

.. toctree::
    :maxdepth: 2
    :caption: Contents

    install
    tags/index
    useful-extensions

Available Tags
==============

The following tags are directly converted to HTML:

- **Images:** Includes an image, with additional parameters for alternative text, wrapping, captions, and source links. Kordac also remembers all images that have found within image tags, which is useful for later checking if all files exist.
- **Videos:** Embeds a YouTube or Vimeo video from a given URL.
- **Text boxes:** Wraps the given content within a block that can be styled by CSS.
- **Panels:** Wraps the given content in a container with an optional header. Panels can be collapsed by JS, and a parameter allows the panel to be collapsed or expanded on page load.

The following tags convert to placeholders to be used by the Django template engine:

- **Static file links:** When linking to a specific static file, this tag will prepend a placeholder for the Django static files path.
- **Numbered Headings:**
- **Interactives:**
- **Table of contents:**
- **Conditional content:**

Kordac also includes the following tags

- **Glossary Entries:**
- **Comments:**

Other Features
==============

- HTML for any given tag can replaced
- Specific tags can be enabled while ignoring all other tags

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
