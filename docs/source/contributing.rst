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
For an overview on how to use kordac, refer to the usage page of these docs.

Kordac is split into <> main parts:

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
    Inherits the `Extension` class from Markdown.
    This class is the main class of the project. It loads all the processor information, loads the template files and clears and populates the attributes to be returned by the ``KordacResult`` object.

- ``Processors/``
  	Each processor is independent from all other processors. There are several different kinds of processors, the types used in Kordac so far are ``preprocessor``, ``blockprocessor``, ``inlinepattern`` and ``treeprocessor``.
  	
  	- What does a processor actually do
  	- Order
  	- Types

- ``Templates/``
  	The jinja templates to be populated by processors.

- ``processor-info.json``

Kordac is an extension for `Python Markdown`_.

.. _Python Markdown: https://pythonhosted.org/Markdown/




Creating a New Processor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To create a new processor, a good place to start is the `Extension API`_ page of the Python docs, or even the `source code`_ itself.

.. _Extension API: https://pythonhosted.org/Markdown/extensions/api.html

.. _source code: https://github.com/waylan/Python-Markdown

There are several different kinds of processors available, each serving a slightly different purpose.

Generally, every processor will have an ``__init__``, ``test`` and ``run`` method.

The processors are called from the ``KordacExtension`` class.

Where do I add my processor to kordac, so that kordac knows to use it? (default processors)
What order do processors happen in?
How do I chose what type of processor to use?
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


Talk about Base classes that we provide.
Want to know why type of tests we want. (Check input and output)

Bug fix? Add tests.



Adding something that interacts with something else? Best to catch those interactions downstream - don't change things at the start of the pipeline to try and get things ready for a processor later on, let that second processor deal with it.