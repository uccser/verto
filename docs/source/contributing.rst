Contributing to Kordac
#######################################

The git repository for Kordac can be found here_.

.. _here: https://github.com/uccser/kordac


Issue Reporting
=======================================
If you come across a bug in Kordac, please `report it`_ on the repo.

.. _report it: https://github.com/uccser/kordac/issues

The Code Base
=======================================
If you would like to contribute to Kordac, fork the repository.

Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Before reading this section, make sure you have read `how to use Kordac`_ (or even better, have already used Kordac!).

.. _how to use Kordac: http://kordac.readthedocs.io/en/develop/usage.html


There are several parts and terms of Kordac to become familiar with:

- **Tag**
    This refers to the custom markdown syntax that Kordac processes.
    
    For example:
    
    .. code-block:: none

      {comment this will be removed by the converter}

      {image file-path='img/totally-real-image.png' alt='process me'}
    
    are examples of the ``comment`` and ``image`` tags in Kordac.  

- ``Kordac()``
	The convertor object itself. This is what a user will use to create a Kordac converter, and what is used to define a custom processor list, custom html templates and custom Markdown Extensions to use.

- ``KordacResult()``
    The object returned by ``Kordac()`` containing:
    	- Converted html string
    	- Title
    	- Required files (images, interactives, scratch images, page scripts)
    	- Heading tree
    	- Required glossary terms

- ``KordacExtension()``
    Inherits the ``Extension`` class from Markdown.
    This class is the main class of the project. It loads all the processor information, loads the template files and clears and populates the attributes to be returned by the ``KordacResult`` object.

- ``Processors/``
  	There is a different processor for each tag. A processor uses it's corresponding regex loaded from ``processor-info.json`` to find matches in the text, and uses the given arguments in the matched tag to populate and output it's html template.

- ``html-templates/``
  	The html templates (using Jinja2 template engine) to be populated by processors.

- ``processor-info.json``
	Every processor is listed in this file, and will at least contain a regex pattern to match it's corresponding tag.
	Most will also define required and optional parameters, these correspond to arguments in the tag's template.



Creating a New Processor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To create a new processor, a good place to start is the `Extension API`_ page of the Python Markdown docs, or even the `source code`_ itself.

.. _Extension API: https://pythonhosted.org/Markdown/extensions/api.html

.. _source code: https://github.com/waylan/Python-Markdown


There are several different kinds of processors in Python Markdown, each serving a slightly different purpose. We recommend reading the API docs to determine which processor best suits your purpose (Kordac currently makes use of ``preprocessor``, ``blockprocessor``, ``inlinepattern`` and ``treeprocessor``).

The order of the processors matters and is defined when each processor is added to the ``OrderedDict`` in ``KordacExtension.py``. Each processor is independent of every other processor. If you have two processors in the pipeline that may overlap (e.g. codehilite and fencedcode), the second processor must handle whatever the first outputs, i.e. refrain from manipulating the outout of the first processor to help the second.

Every processor belongs in the ``processors/`` directory, but there are several other places they need to be listed, these are:

- The frozenset of ``DEFAULT_PROCESSORS`` in ``Kordac.py``
- The relevant list in ``extendMarkdown()`` in ``KordacExtension.py`` (see `OrderedDict in the Markdown API docs`_ for determining order)
.. _OrderedDict in the Markdown API docs: https://pythonhosted.org/Markdown/extensions/api.html#ordereddict
- The processor's template should be added to ``html-templates`` using the Jinja2 Template Engine syntax for variable parameters
- The processor's relevant information (regex pattern, required parameters etc) should be included in ``processor-info.json``

Generally, every processor will have an ``__init__``, ``test`` and ``run`` method.


  	


Where do I add my processor to kordac, so that kordac knows to use it? (default processors)

Add to processor information file.
What things should remain independent from each other - only a couple things that interact, (required files, headingnode)

Put page in docs, examples of how to use it, how to configure. Required and optional arguments. Jinja template overrides.


The Test Suite
=======================================
To start the test suite:

.. code-block:: none

    $ python3 -m kordac.tests.start_tests

This will execute the Smoke, System and then Unit tests.

To execute the test suite without the smoke tests:

.. code-block:: none

	$ python3 -m kordac.tests.start_tests --no_smoke

Creating a release
=======================================

This is our current process for creating and publishing a Kordac release. This
can only be performed by repository administrators

1. `Create a release branch <http://nvie.com/posts/a-successful-git-branching-model/#creating-a-release-branch>`_. Checkout to this branch.
2. Update the version number [1]_ within ``kordac/__init__.py``.
3. Check test suite for errors, and fix any issues that arise, or `log an issue <https://github.com/uccser/cs-field-guide/issues/new>`_.
4. Detail the changes in ``docs/source/changelog.rst``.
5. `Complete the release branch <http://nvie.com/posts/a-successful-git-branching-model/#finishing-a-release-branch>`_. Be sure to tag the release with the version number for creating the release on GitHub.
6. Create the release on `GitHub <https://github.com/uccser/kordac/releases/>`_ on the tagged commit.
7. Upload a new version of Kordac to PyPI.

.. [1] We follow `Semantic Versioning <http://semver.org/>`_ for our numbering system. The number is used by ``setup.py`` to tell PyPI which version is being uploaded or ``pip`` which version is installed, and also used during the documentation build to number the version of Kordac it was built from.

Notes
=======================================

Talk about Base classes that we provide.
Want to know why type of tests we want. (Check input and output)

Bug fix? Add tests.



Adding something that interacts with something else? Best to catch those interactions downstream - don't change things at the start of the pipeline to try and get things ready for a processor later on, let that second processor deal with it.
