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

Creating a release
=======================================

This is our current process for creating and publishing a Kordac release. This
can only be performed by users that are part of the `uccser/Kordac team`, if you
are not on this team get in contact with someone who is.

1. `Create a release branch <http://nvie.com/posts/a-successful-git-branching-model/#creating-a-release-branch>`_. Checkout to this branch.
2. Update the version number [1]_ within ``kordac/__init__.py``.
3. Check test suite for errors, and fix any issues that arise, or `log an issue <https://github.com/uccser/cs-field-guide/issues/new>`_.
4. Detail the changes in ``docs/source/changelog.rst``.
5. `Complete the release branch <http://nvie.com/posts/a-successful-git-branching-model/#finishing-a-release-branch>`_. Be sure to tag the release with the version number for creating the release on GitHub.
6. Create the release on `GitHub <https://github.com/uccser/kordac/releases/>`_ on the tagged commit.
7. Upload a new version of Kordac to PyPI.

.. [1] We follow `Semantic Versioning <http://semver.org/>`_ for our numbering system. The number is used by ``setup.py`` to tell PyPI which version is being uploaded or ``pip`` which version is installed.
