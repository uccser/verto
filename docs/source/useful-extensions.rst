Useful Extensions
#######################################

This page details useful extensions to pass to Kordac to enable extra rendering capabilities. As Kordac is an extension of the Python Markdown package, you should be able to include any extension for the original package.

To include a package, pass a list of extensions to the ``extensions`` parameter when creating the Kordac object. For example:

.. code-block:: python

    extra_extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.sane_lists',
        mdx_math.MathExtension(enable_dollar_delimiter=True)
    ]
    converter = Kordac(extensions=extra_extensions)



Math
=======================================

Math can be rendered by including the `Python Markdown Math <https://pypi.python.org/pypi/python-markdown-math>`_ package, and passing it through to Kordac as an extension to run. A guide on how to install and use the extension can be found in the package's `README file <https://github.com/mitya57/python-markdown-math/blob/master/README.md>`_.
