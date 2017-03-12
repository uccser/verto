Contributing to Kordac
#######################################

Welcome to the Kordac developer community! We have spent many months developing this project, and we would love for you to get involved! The following documentation has been written to help you get a grasp on how Kordac is pieced together to make contributing as simple and straight forward as possible. Please feel free to fix bugs and/or suggest new features and improvements to the system (or the docs) by making a pull request.

Kordac was created to be used by two much larger projects (the `CS Unplugged`_ and `CS Field Guide`_ websites) as the markdown-to-html converter. The tags we chose are designed to allow authors of these two projects to easily write material without technical elements getting in the way. It is therefore important to us that Kordac remains as simple and robust as possible, please keep this in mind if you decide to work on Kordac with us.

The git repository for Kordac can be found `here`_, jump in and take a look around!

.. note::

	The two projects that Kordac was developed for are Django projects, so you may come across HTML (in templates, test cases etc) that contains Django syntax.

	For example, below is the expected output for a for a image tag test:

	.. code-block:: HTMl

		<div>
		 <img alt="Lipsum" class="" src="{% static 'computer-studying-turing-test.png' %}"/>
		</div>

	This does not mean that Kordac is only suitable for Django projects, as it's just a matter of customising the relevant HTMl templates.


Issue Reporting and Bug Fixes
=======================================

If you come across a bug in Kordac, please `report it on the repo issue tracker`_.

If you choose to fix the bug for us, consider adding the relevant tests to the Test Suite (detailed further down this page) to help us catch any future bugs.


The Code Base
=======================================

If you would like to contribute to Kordac, `create a fork of the repository`_.


Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before reading this section, make sure you have read `how to use Kordac`_ (or even better, have already used Kordac!).


Terminology
***************************************

There are a couple of terms we use when describing Kordac to become familiar with:

- **Tag**
    This refers to the custom markdown syntax that Kordac processes.
    
    For example:
    
    .. code-block:: none

      {comment this will be removed by the converter}

      {image file-path="img/totally-real-image.png" alt="process me"}
    
    are examples of the ``comment`` and ``image`` tags in Kordac.

- **Processor**
	This refers to the class that is responsible for converting a specific tag. For example, ``RelativeLinkPattern`` is the processor for internal links.


Project Structure
***************************************

Below is a basic overview of the project structure:

.. code-block:: none

	├── docs/
	├── kordac/
	│   ├── html-templates/
	│   ├── KordacExtension.py
	│   ├── Kordac.py
	│   ├── processor-info.json
	│   ├── processors/
	│   │   └── errors/
	│   ├── tests/
	│   └── utils/
	├── requirements.txt
	└── setup.py

The items of interest are:

- ``Kordac()``
	The convertor object itself. This is what a user will use to create a Kordac converter, and what is used to define a custom processor list, custom html templates and custom Markdown Extensions to use.

- ``KordacResult()`` (found in ``Kordac.py``)
    The object returned by ``Kordac()`` containing:
    	- Converted html string
    	- Title
    	- Required files (images, interactives, scratch images, page scripts)
    	- Heading tree
    	- Required glossary terms

- ``KordacExtension()``
    This is the main class of the project, and inherits the ``Extension`` class from Markdown.
    It loads all of the processor information, loads the template files and clears and populates the attributes to be returned by the ``KordacResult`` object.

- ``Processors/``
  	There is a different processor for each tag. A processor uses it's corresponding regex loaded from ``processor-info.json`` to find matches in the text, and uses the given arguments in the matched tag to populate and output it's html template.

- ``html-templates/``
  	The html templates (using the Jinja2 template engine) with variable arguments to be populated by processors.

- ``processor-info.json``
	Every processor is listed in this file, and will at least contain a regex pattern to match it's corresponding tag.
	Most will also define required and optional parameters, these correspond to arguments in the tag's html template.

- ``tests/`` are explained in the Test Suite section further down the page.


It is important to note that Kordac is not just a Markdown Extension, it is a wrapper for Python Markdown. ``KordacExtension`` **is** an extension for Python Markdown. We have created a wrapper because we wanted to not only convert text, but also extract information from the text as it was being converted (recall ``KordacResult()`` listed above).


Creating a New Processor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a new processor, a good place to start is the `Extension API`_ page of the Python Markdown docs, and you can also read the `source code`_ itself.

There are several different kinds of processors in Python Markdown, each serving a slightly different purpose. We recommend reading the API docs to determine which processor best suits your purpose. Kordac currently makes use of ``preprocessor``, ``blockprocessor``, ``inlinepattern``, ``treeprocessor`` and ``postprocessor``, but you are welcome to use another type of processor if it better suits the task.

The order of the processors matters and is defined when each processor is added to the ``OrderedDict`` in ``KordacExtension.py``.

Each processor should try to be as independent of every other processor as possible. Sometimes this is not possible, and in this case compatibility should occur in the processor that happens last (i.e. the downstream processor). That is output should be consistent based on input, not the other way round (e.g. ``codehilite`` and ``fenced_code``).

The logic for each processor belongs in the ``processors/`` directory, and there are several other places where processors details need to be listed. These are:

- The processor's relevant information (regex pattern, required parameters etc) should be included in ``processor-info.json``
- If it should be a default processor, it should be added to the frozenset of ``DEFAULT_PROCESSORS`` in ``Kordac.py``
- The relevant list in ``extendMarkdown()`` in ``KordacExtension.py`` (see `OrderedDict in the Markdown API docs`_ for manipulating processor order)
- The processor's template should be added to ``html-templates`` using the Jinja2 template engine syntax for variable parameters

The new processors should also:

- Be thoroughly tested (see the section below)
- Have clear and accurate documentation. See the docs on other processors for the preferred format. Your docs should include:
	- An example of the tag in markdown
	- Required parameters
	- Optional parameters
	- Examples
	- Examples of overriding the html

We recommend writing documentation and test cases before you even write the processor itself as this will give you a clear idea of how a processor in Kordac should behave.


The Test Suite
=======================================

To start the test suite:

.. code-block:: bash

    $ python3 -m kordac.tests.start_tests

This will execute the Smoke, System and then Unit tests.

There are several arguments that can be used with this command to skip particular tests (``--no_smoke``, ``--no_system`` and ``--no_unit``).

Test Suite Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are now focusing on our project structure diagram from earlier:

.. code-block:: none

	└── kordac/
	    └── tests/
	        ├── assets/
	        ├── BaseTest.py
	        ├── ConfigurationTest.py
	        ├── ProcessorTest.py
	        ├── SmokeTests.py
	        └── start_tests.py

The items of interest are:

- ``BaseTest())``
	This class is inherited by nearly every other test file, and contains a method to read a given test asset file.

- ``ConfigurationTest()``
	This is the test class for testing different configurations of ``Kordac()`` (e.g. using a custom list of processors and/or custom html templates). This class inherits the ``BaseTest`` class.

- ``ProcessorTest.py``
	This is the class inherited by all processor test classes. It contains several useful methods for testing processors, including those for loading templates and processor info.

- ``SmokeDocsTest()`` and ``SmokeFileTest()``
	These are the two classes for smoke testing.

- ``start_tests.py``
	This is the file that is executed in order to run each of the three types of tests (Smoke, System and Unit). Every new test class must be added to the relevant section of this file.

- ``assets/``
	This directory contains a sub directory for every test class that loads external assets (e.g. test input files).


Adding Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When writing a new test function, it is important that the method name is as descriptive as possible. The method name should also be prefixed with ``test_`` as the test suite will only execute methods with this prefix.

If you have added a new processor to ``Kordac``, then a corresponding test suite also needs to be added. This test suite should be added to the ``unit_suite()`` function in ``start_tests.py``. The section below has details on how to write a processor test.
	

Processor Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All processor tests inherit from the ``ProcessorTest`` class. Processors should create a ``Mock()`` object, which will contain the bare minimum for the processor to be run (it's HTML template and properties loaded from ``processor-info.json``), i.e. there is no reason for it to know about properties of the other processors.

A test method will typically follow the same sequence of steps:

	1. Retrieve the test string (there is a ``read_test_file()`` method provided by the ``ProcessorTest`` class)
	2. Confirm there are (not) matches to the regex in the test string
	3. Convert the test string using the ``kordac_extension`` (provided by the ``SetUp()`` method in ``ProcessorTest``)
	4. Load the expected converted result
	5. Check the converted result is the same as the expected result


Testing Assets
***************************************

Most tests will load an asset file. This file contains example Markdown text (and therefore has a ``.md`` extension). For comparing the converted result of this Markdown file with it's expected output, a corresponding "expected" file should be created. The expected file should have the same name as the corresponding test file, with ``expected`` appended to the file name (and has a ``.html`` extension).

These asset files should be placed in ``kordac/tests/assets/<processor-name>/``. 

For example:

.. code-block:: none
	
	kordac/tests/assets/boxed-text/no_boxed_text.md
	kordac/tests/assets/boxed-text/no_boxed_text_expected.html

.. note::
	- Asset files should have discriptive names, and in many cases will have the same name as the method they are used in.

Creating a release
=======================================

This is our current process for creating and publishing a Kordac release. This
can only be performed by repository administrators

1. `Create a release branch`_. Checkout to this branch.
2. Update the version number [1]_ within ``kordac/__init__.py``.
3. Check test suite for errors, and fix any issues that arise, or `log an issue`_.
4. Detail the changes in ``docs/source/changelog.rst``.
5. `Complete the release branch`_. Be sure to tag the release with the version number for creating the release on GitHub.
6. Create the release on `GitHub`_ on the tagged commit.
7. Upload a new version of Kordac to PyPI.

.. [1] We follow `Semantic Versioning <http://semver.org/>`_ for our numbering system. The number is used by ``setup.py`` to tell PyPI which version is being uploaded or ``pip`` which version is installed, and also used during the documentation build to number the version of Kordac it was built from.


Notes
=======================================

Kordac should make use GitHub's features:

Issue template
Pull request template
Contributing page
So GitHub can display these when appropriate.

.. _CS Unplugged: https://github.com/uccser/cs-unplugged/
.. _CS Field Guide: https://github.com/uccser/cs-field-guide/
.. _here: https://github.com/uccser/kordac
.. _report it on the repo issue tracker: https://github.com/uccser/kordac/issues
.. _create a fork of the repository: https://help.github.com/articles/fork-a-repo/
.. _how to use Kordac: http://kordac.readthedocs.io/en/develop/usage.html
.. _Extension API: https://pythonhosted.org/Markdown/extensions/api.html
.. _source code: https://github.com/waylan/Python-Markdown
.. _OrderedDict in the Markdown API docs: https://pythonhosted.org/Markdown/extensions/api.html#ordereddict
.. _Create a release branch: http://nvie.com/posts/a-successful-git-branching-model/#creating-a-release-branch
.. _log an issue: https://github.com/uccser/cs-field-guide/issues/new
.. _Complete the release branch: http://nvie.com/posts/a-successful-git-branching-model/#finishing-a-release-branch
.. _GitHub: https://github.com/uccser/kordac/releases/