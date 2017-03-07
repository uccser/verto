Contributing to Kordac
#######################################

The git repository for Kordac can be found here_.

.. _here: https://github.com/uccser/kordac


Issue Reporting
=======================================
If you come across a bug in Kordac, please report it on the GitHub repository_.

.. _repository: https://github.com/uccser/kordac/issues

The Code Base
=======================================
If you would like to contribute to Kordac, fork the repository.

Kordac is an extension for `Python Markdown`_.

.. _Python Markdown: https://pythonhosted.org/Markdown/


< what does kordac return >
< how is kordac called >


Creating a New Processor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To create a new processor, a good place to start is the `Extension API`_ page of the Python docs, or even the `source code`_ itself.

.. _Extension API: https://pythonhosted.org/Markdown/extensions/api.html

.. _source code: https://github.com/waylan/Python-Markdown

There are several different kinds of processors available, each serving a slightly different purpose.

Generally, every processor will have an ``__init__``, ``test`` and ``run`` method.

The processors are called from the ``KordacExtension`` class.

The Test Suite
=======================================
To start the test suite:

.. code-block:: none

    $ python3 -m kordac.tests.start_tests

This will execute the Smoke, System and then Unit tests.

To execute the test suite without the smoke tests:

.. code-block:: none

	$ python3 -m kordac.tests.start_tests --no_smoke
