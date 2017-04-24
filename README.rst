|Verto Image|

|Build Status| |Code Climate Status|

Verto is an extension of the Python Markdown package, which allows
authors to include complex HTML elements with simple text tags in their
Markdown files.

Basic Usage
-----------

Verto allows for an author to quickly include images and content and display
them in a panel (similar to a Bootstrap Collapsible Panel) with the following
markdown:

.. code-block::

  # Example Header

  Example Paragraph

  {panel type="example" title="Example Panel"}

  {image file-path="http://placehold.it/350x150" caption="Example Image"}

  {panel end}

While Verto has many configuration options it can be used immediately
with little code. For example, if the previous markdown is saved in the file
called ``example.md`` then the following would convert that file and print the
output to stdout:

.. code-block:: python

  from verto import Verto

  text = open('example.md', 'r')
  converter = Verto()
  result = converter.convert(text)

  print(result.html_string)

Documentation
-------------

Installation and usage documentation for Verto can be found on
`ReadTheDocs`_, and can also be built from the documentation source
within the ``docs/`` directory of the development distribution.

License
-------

Verto is licensed under the MIT License. Read the `license file`_ for
more details.

Bugs and feature requests
-------------------------

Have a bug or a feature request? Please first search for `existing and
closed issues`_ in our issue tracker. If your problem or idea is not
addressed yet, please `open a new issue`_.

FAQ
---

**Where is the changelog?**

The changelog is available within the `documentation`_.

**How do I install the development version as local package?**

1. ``$ git clone https://github.com/uccser/verto.git``
2. ``$ cd verto``
3. ``$ pip3 install .``

.. _ReadTheDocs: http://verto.readthedocs.io/en/latest/
.. _documentation: http://verto.readthedocs.io/en/latest/changelog.html
.. _license file: LICENSE.md
.. _existing and closed issues: https://github.com/uccser/verto/issues
.. _open a new issue: https://github.com/uccser/verto/issues/new

.. |Build Status| image:: https://travis-ci.org/uccser/verto.svg?branch=master
   :target: https://travis-ci.org/uccser/verto

.. |Code Climate Status| image:: https://codeclimate.com/github/uccser/verto/badges/gpa.svg
  :target: https://codeclimate.com/github/uccser/verto
  :alt: Code Climate

.. |Verto Image| image:: https://raw.githubusercontent.com/uccser/verto/master/verto/images/verto-logo.png
  :target: https://github.com/uccser/verto
  :alt: Verto GitHub
