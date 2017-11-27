Contributing to Verto
#######################################

Welcome to the Verto developer community! We have spent many months developing this project, and we would love for you to get involved! The following documentation has been written to help you get a grasp on how Verto is pieced together to make contributing as simple and straight forward as possible. Please feel free to fix bugs and/or suggest new features and improvements to the system (or the docs) by making a pull request.

Verto was created to be used by two much larger projects (the `CS Unplugged`_ and `CS Field Guide`_ websites) as the markdown-to-html converter. The tags we chose are designed to allow authors of these two projects to easily write material without technical elements getting in the way. It is therefore important to us that Verto remains as simple and robust as possible, please keep this in mind if you decide to work on Verto with us.

The git repository for Verto can be found `here`_, jump in and take a look around!

.. note::

  The two projects that Verto was developed for are Django projects, so you may come across HTML (in templates, test cases etc) that contains Django syntax.

  For example, below is the expected output for a for a image tag test:

  .. code-block:: HTMl

      <div>
       <img alt="Lipsum" class="" src="{% static 'computer-studying-turing-test.png' %}"/>
      </div>

  This does not mean that Verto is only suitable for Django projects, as it's just a matter of customising the relevant HTMl templates.


Issue Reporting and Bug Fixes
=======================================

If you come across a bug in Verto, please `report it on the repo issue tracker`_.

If you choose to fix the bug for us, consider adding the relevant tests to the Test Suite (detailed further down this page) to help us catch any future bugs.


The Code Base
=======================================

If you would like to contribute to Verto, `create a fork of the repository`_.


Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before reading this section, make sure you have read :doc:`how to use <usage>` (or even better, have already used Verto!).


Terminology
***************************************

There are a couple of terms we use when describing Verto to become familiar with:

- **Tag**

  This refers to the custom markdown syntax that Verto processes.

  For example:

  .. code-block:: none

    {comment this will be removed by the converter}

    {image file-path="img/totally-real-image.png" alt="process me"}

  are examples of the ``comment`` and ``image`` tags in Verto.

- **Processor**

  This refers to the class that is responsible for converting a specific tag. For example, ``RelativeLinkPattern`` is the processor for internal links.


Project Structure
***************************************

Below is a basic overview of the project structure:

.. code-block:: none

  ├── docs/
  ├── verto/
  |   ├── errors/
  │   ├── html-templates/
  │   ├── VertoExtension.py
  │   ├── Verto.py
  │   ├── processor-info.json
  │   ├── processors/
  │   ├── tests/
  │   └── utils/
  ├── requirements.txt
  └── setup.py

The items of interest are:

- ``Verto()`` - The convertor object itself. This is what a user will use to create a Verto converter, and what is used to define a custom processor list, custom html templates and custom Markdown Extensions to use.

- ``VertoResult()`` (found in ``Verto.py``) - The object returned by ``Verto()`` containing:

  - Converted html string
  - Title
  - Required files (images, interactives, scratch images, page scripts)
  - Heading tree
  - Required glossary terms

- ``VertoExtension()`` - This is the main class of the project, and inherits the ``Extension`` class from Markdown. It loads all of the processor information, loads the template files and clears and populates the attributes to be returned by the ``VertoResult`` object.

- ``processor-info.json`` - Every processor is listed in this file, and will at least contain a class determining whether it is custom or generic, where custom processors will have a pattern to match it's corresponding tag. Most will also define required and optional parameters, these correspond to arguments in the tag's html template.

- ``processors/`` - There is a different processor for each tag. A processor uses it's corresponding description loaded from ``processor-info.json`` to find matches in the text, and uses the given arguments in the matched tag to populate and output it's html template.

- ``html-templates/`` - The html templates (using the Jinja2 template engine) with variable arguments to be populated by processors.

- ``errors/`` - Contains all the errors exposed by the Verto module. Where an Error is an exception that is caused by user input. New errors should be created in here inheriting from the base ``Error`` class.

- ``utils/`` - Contains classes and methods not necessarily unique to Verto that are useful in any sub-module. This includes slugify handlers, html parsers and serialisers, and other utilities. The utilities should be used over external libraries as they are purposely built because of: compatibility reasons, licensing restrictions, and/or unavailability of require features.

- ``tests/`` - explained in the Test Suite section further down the page.

It is important to note that Verto is not just a Markdown Extension, it is a wrapper for Python Markdown. ``VertoExtension`` **is** an extension for Python Markdown. We have created a wrapper because we wanted to not only convert text, but also extract information from the text as it was being converted (recall ``VertoResult()`` listed above).


Creating a New Processor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways distinctly different ways to create a new processor. The simplist way is to make use of the provided generic processors and define the new processor in the ``processor-info.json`` file, while more complex processors reqiure additional source code. Complex processors should be considered when custom functionality is required that cannot be achieved with generic processors.

In all cases new processors should:

- Be thoroughly tested (see the section on :ref:`testing <the-test-suite>`)
- Have clear and accurate documentation. See the docs on other processors for the preferred format. Your docs should include:

  - An example of the tag in markdown
  - Required parameters
  - Optional parameters
  - Examples
  - Examples of overriding the html

We recommend writing documentation and test cases before you even write the processor itself as this will give you a clear idea of how a processor in Verto should behave.

Generic Processors
**************************************

There are two types of generic processors:

  - tags (``generic_tag``): which match ``{<processor_name> <args>}`` in the markdown text replacing with the given html-template.
  - containers (``generic_container``): which are a pair of tags which capture the content between the tags for the html-template. A generic container's opening tag specifies the arguments, while the closing tag only has the ``end`` argument allowing for the content to contain generic containers.

To create a new processor that uses the generic processors the processor must be added to the ``processor-info.json`` file and an associated html-template must be created. The template must only have one root level node after rendering.

How to make a JSON Definition
++++++++++++++++++++++++++++++++++++++

The json description of a generic processor must contain the attributes:

  - ``class``: Either ``generic_tag`` or ``generic_container`` for a generic processor.
  - ``arguments``: An object describing arguments passed to the tag.
  - ``template_parameters``: An object describing template parameters.
  - (Optional) ``template_name``: A custom name for the html-template to use. Defaults to the processor name otherwise.
  - (Optional) ``tag_argument``: The text given at the beginning of a tag (e.g. the tag argument for ``{image file-path="example.png"}`` is ``image``). This is only necessary for processors with different names sharing the same resources (e.g. both ``image-container`` and ``image-tag`` share the ``image.html`` template).

The ``argument`` parameter is a dictionary (or object) containing argument name, argument-info pairs. Where the argument-info contains the attributes:

  - ``required``: ``true`` if the argument must be set or ``false`` otherwise.
  - (Optional) ``dependencies``: A list of argument-names that must also be set if this argument is used.
  - (Optional) ``values``: A list of values of which the argument may take. If the argument does not have the value in this list the ArgumentValueError exception is raised.

These arguments are transformed for use in the html-template by the ``template_parameters`` attribute. This attribute is similar to the ``argument`` attribute by containing parameter name, parameter-info pairs. Where the parameter-info contains the attributes:

  - ``argument``: The name of the argument to retrieve the value of to  use/transform into the parameter value.
  - (Optional) ``default``: The value the parameter defaults to if the argument is not given otherwise defaults to ``None``.
  - (Optional) ``transform``: The name of the transform to modify the argument value by or defaults to null for no transformation. The avaliable transforms are detailed below.
  - (Optional) ``transform_condition``: A function that takes the context after parameters are set but before transformation (The transformations are done in order they appear in the json document). If the function returns ``True`` then the transformation is applied.

For a generic container type processor the ``argument`` of the parameter may be ``content`` which is the captured content between the start and end tags.

The set of currently avaliable transformations for the ``transform`` attribute are:

  - ``str.lower``: Converts the string into a lowercase version.
  - ``str.upper``: Converts the string into an UPPERCASE version.
  - ``relative_file_link``: Applies the relative-file-link html-template to the argument.

Examples
++++++++++++++++++++++++++++++++++++++

A generic tag processor, is a simple single line tag that uses the given arguments as parameters to an html template. An example of a processor that uses the generic tag processor is the :ref:`button-link <button-link>` processor which is described in the json as:

.. code-block:: none

    "button-link": {
      "class": "generic_tag",
      "arguments": {
        "link": {
          "required": true,
          "dependencies": []
        },
        "text": {
          "required": true,
          "dependencies": []
        },
        "file": {
          "required": false,
          "dependencies": []
        }
      },
      "template_parameters": {
        "file": {
          "argument": "file",
          "transform": "str.lower",
          "default": "no"
        },
        "link": {
          "argument": "link",
          "transform": "relative_file_link",
          "transform_condition": "lambda context: context['file'] == 'yes'"
        },
        "text": {
          "argument": "text",
          "transform": null
        }
      }
    }

And has the following html-template:

.. literalinclude:: ../../verto/html-templates/button-link.html
    :language: css+jinja

This enables the following markdown:

.. literalinclude:: ../../verto/tests/assets/button-link/doc_example_basic_usage.md
    :language: none

To generate the output:

.. literalinclude:: ../../verto/tests/assets/button-link/doc_example_basic_usage_expected.html
    :language: html

A generic container processor, a pair of matching tags where one opens the container and one closes the container. The start tag gives the arguments as parameters to an html template. The end tag is used to capture the content between the tags to be used as an additional parameter to the html template.  An example of a processor that uses the generic container processor is the :ref:`boxed-text <boxed-text>` processor which is described in the json as:

.. code-block:: none

    "boxed-text": {
        "class": "generic_container",
        "arguments": {
          "indented": {
            "required": false,
            "dependencies": []
          }
        },
        "template_name": "boxed-text",
        "template_parameters": {
          "indented": {
            "argument": "indented",
            "transform": "str.lower"
          },
          "text": {
            "argument": "content",
            "transform": null
          }
        }
    }

And has the following html-template:

.. literalinclude:: ../../verto/html-templates/boxed-text.html
    :language: css+jinja

This enables the following markdown:

.. literalinclude:: ../../verto/tests/assets/boxed-text/doc_example_basic_usage.md
    :language: none

To generate the output:

.. literalinclude:: ../../verto/tests/assets/boxed-text/doc_example_basic_usage_expected.html
    :language: html

Custom Processors
**************************************

To create a custom processor, the ``class`` attribute of the processor in the ``processor-info.json`` file must be ``"custom"``. A good place to start when programming a new processor is the `Extension API`_ page of the Python Markdown docs, and you can also read the `source code`_ itself.

There are several different kinds of processors in Python Markdown, each serving a slightly different purpose. We recommend reading the API docs to determine which processor best suits your purpose. Verto currently makes use of ``preprocessor``, ``blockprocessor``, ``inlinepattern``, ``treeprocessor`` and ``postprocessor``, but you are welcome to use another type of processor if it better suits the task.

The order of the processors matters and is defined when each processor is added to the ``OrderedDict`` in ``VertoExtension.py``.

Each processor should try to be as independent of every other processor as possible. Sometimes this is not possible, and in this case compatibility should occur in the processor that happens last (i.e. the downstream processor). That is output should be consistent based on input, not the other way round (e.g. ``codehilite`` and ``fenced_code``).

The logic for each processor belongs in the ``processors/`` directory, and there are several other places where processors details need to be listed. These are:

- The processor's relevant information (regex pattern, required parameters etc) should be included in ``processor-info.json``.
- If it should be a default processor, it should be added to the frozenset of ``DEFAULT_PROCESSORS`` in ``Verto.py``.
- The relevant list in ``extendMarkdown()`` in ``VertoExtension.py`` (see `OrderedDict in the Markdown API docs`_ for manipulating processor order).
- The processor's template should be added to ``html-templates`` using the Jinja2 template engine syntax for variable parameters. A valid template will only have one root level node after rendering, if more root nodes are necessary the remove tag can be used as the root node which will be removed later.
- Any errors should have appropriate classes in the ``errors\`` directory, they should be well described by their class name such that for an expert knows immediately what to do to resolve the issue, otherwise a message should be used to describe the exact causation of the error for a novice.


.. _the-test-suite:

The Test Suite
=======================================

To start the test suite:

.. code-block:: bash

  $ python3 -m verto.tests.start_tests

This will execute the Smoke, System and then Unit tests.

There are several arguments that can be used with this command to skip particular tests (``--no_smoke``, ``--no_system`` and ``--no_unit``).

Test Suite Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are now focusing on our project structure diagram from earlier:

.. code-block:: none

    └── verto/
        └── tests/
            ├── assets/
            ├── BaseTest.py
            ├── ConfigurationTest.py
            ├── ProcessorTest.py
            ├── SmokeTests.py
            └── start_tests.py

The items of interest are:

- ``BaseTest())`` - This class is inherited by nearly every other test file, and contains a method to read a given test asset file.

- ``ConfigurationTest()`` - This is the test class for testing different configurations of ``Verto()`` (e.g. using a custom list of processors and/or custom html templates). This class inherits the ``BaseTest`` class.

- ``ProcessorTest.py`` - This is the class inherited by all processor test classes. It contains several useful methods for testing processors, including those for loading templates and processor info.

- ``SmokeDocsTest()`` and ``SmokeFileTest()`` - These are the two classes for smoke testing.

- ``start_tests.py`` - This is the file that is executed in order to run each of the three types of tests (Smoke, System and Unit). Every new test class must be added to the relevant section of this file.

- ``assets/`` - This directory contains a sub directory for every test class that loads external assets (e.g. test input files).


Adding Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When writing a new test function, it is important that the method name is as descriptive as possible. The method name should also be prefixed with ``test_`` as the test suite will only execute methods with this prefix.

If you have added a new processor to ``Verto``, then a corresponding test suite also needs to be added. This test suite should be added to the ``unit_suite()`` function in ``start_tests.py``. The section below has details on how to write a processor test.


Processor Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All processor tests inherit from the ``ProcessorTest`` class. Processors should create a ``Mock()`` object, which will contain the bare minimum for the processor to be run (it's HTML template and properties loaded from ``processor-info.json``), i.e. there is no reason for it to know about properties of the other processors.

A test method will typically follow the same sequence of steps:

1. Retrieve the test string (there is a ``read_test_file()`` method provided by the ``ProcessorTest`` class)
2. Confirm there are (not) matches to the regex in the test string
3. Convert the test string using the ``verto_extension`` (provided by the ``SetUp()`` method in ``ProcessorTest``)
4. Load the expected converted result
5. Check the converted result is the same as the expected result


Testing Assets
***************************************

Most tests will load an asset file. This file contains example Markdown text (and therefore has a ``.md`` extension). For comparing the converted result of this Markdown file with it's expected output, a corresponding "expected" file should be created. The expected file should have the same name as the corresponding test file, with ``expected`` appended to the file name (and has a ``.html`` extension).

These asset files should be placed in ``verto/tests/assets/<processor-name>/``.

For example:

.. code-block:: none

  verto/tests/assets/boxed-text/no_boxed_text.md
  verto/tests/assets/boxed-text/no_boxed_text_expected.html

.. note::
  - Asset files should have discriptive names, and in many cases will have the same name as the method they are used in.

Creating a release
=======================================

This is our current process for creating and publishing a Verto release. This
can only be performed by repository administrators

1. `Create a release branch`_. Checkout to this branch.
2. Update the version number [1]_ within ``verto/__init__.py``.
3. Check test suite for errors, and fix any issues that arise, or `log an issue`_.
4. Detail the changes in ``docs/source/changelog.rst``.
5. `Complete the release branch`_. Be sure to tag the release with the version number for creating the release on GitHub.
6. Create the release on `GitHub`_ on the tagged commit.
7. Upload a new version of Verto to PyPI.

.. [1] We follow `Semantic Versioning <http://semver.org/>`_ for our numbering system. The number is used by ``setup.py`` to tell PyPI which version is being uploaded or ``pip`` which version is installed, and also used during the documentation build to number the version of Verto it was built from.


.. _CS Unplugged: https://github.com/uccser/cs-unplugged/
.. _CS Field Guide: https://github.com/uccser/cs-field-guide/
.. _here: https://github.com/uccser/verto
.. _report it on the repo issue tracker: https://github.com/uccser/verto/issues
.. _create a fork of the repository: https://help.github.com/articles/fork-a-repo/
.. _Extension API: https://pythonhosted.org/Markdown/extensions/api.html
.. _source code: https://github.com/waylan/Python-Markdown
.. _OrderedDict in the Markdown API docs: https://pythonhosted.org/Markdown/extensions/api.html#ordereddict
.. _Create a release branch: http://nvie.com/posts/a-successful-git-branching-model/#creating-a-release-branch
.. _log an issue: https://github.com/uccser/cs-field-guide/issues/new
.. _Complete the release branch: http://nvie.com/posts/a-successful-git-branching-model/#finishing-a-release-branch
.. _GitHub: https://github.com/uccser/verto/releases/
