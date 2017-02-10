Extensions
#######################################

As Kordac is an extension of the Python Markdown package, you should be able to include any extension for the original package.
This page details using extensions with Kordac, plus listing a few useful extensions that we recommend.

To include a package, pass a list of extensions to the ``extensions`` keyword when creating the Kordac object. For example:

.. code-block:: python

    extra_extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.sane_lists',
        mdx_math.MathExtension(enable_dollar_delimiter=True)
    ]
    converter = Kordac(extensions=extra_extensions)

A list of extensions for the Markdown package can be found `in their official documentation <http://pythonhosted.org/Markdown/extensions/index.html>`_.

Math
=======================================

Math can be rendered by including the `Python Markdown Math <https://pypi.python.org/pypi/python-markdown-math>`_ package, and passing it through to Kordac as an extension to run.
A guide on how to install and use the extension can be found in the package's `README file <https://github.com/mitya57/python-markdown-math/blob/master/README.md>`_.

Fenced Code
=======================================

The Fenced Code Blocks extension adds a secondary way to define code blocks, which overcomes a few limitations of the indented code blocks.
More details on the Fenced Code extension can be found `in their official documentation <http://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html>`_.

Code Highlighting
=======================================

The CodeHilite extension adds code/syntax highlighting to standard Python-Markdown code blocks using Pygments.
More details on the CodeHilite extension can be found `in their official documentation <http://pythonhosted.org/Markdown/extensions/code_hilite.html>`_.

Sane Lists
=======================================

The Sane Lists extension alters the behavior of the Markdown List syntax to be less surprising.
More details on the Sane Lists extension can be found `in their official documentation <http://pythonhosted.org/Markdown/extensions/sane_lists.html>`_.
