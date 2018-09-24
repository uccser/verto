Changelog
#######################################


0.9.2
=======================================
- Resolve issues with deployment to PyPI.

0.9.1
=======================================
- Redeploy Verto to PyPI due to bug in 0.9.0.

0.9.0
=======================================

- Add :doc:`processors/blockquote` processor for customising block quote style.
- Added CodeCov to repo
- Dependency updates:

  - Update ``python-slugify`` to 1.2.6
  - Update ``sphinx`` to 1.8.0

0.8.0
=======================================

- Modify :doc:`processors/interactive` processor for translating text, by required text between start and end tags for whole page interactives.
- Modify Verto parameters available on creation to allow modification of default required parameters for each processor.
- Dependency updates:

  - Update ``setuptools`` to 40.2.0.
  - Update ``sphinx`` to 1.7.7.
  - Update ``sphinx_rtx_theme`` to 0.4.1.

0.7.4
=======================================

- Modify :doc:`processors/interactive` processor to use ``slug`` rather than ``name`` to identify interactives
- Modify :doc:`processors/video` processor template for youtube videos
- Modify :doc:`processors/boxed-text` processor to have optional type parameter
- Update style error message to inclue line numbers
- Dependency updates:

  - Update ``python-slugify`` to 1.2.5.
  - Update ``setuptools`` to 39.1.0.
  - Update ``sphinx`` to 1.6.6.
  - Update ``sphinx_rtx_theme`` to 0.3.0.

0.7.3
=======================================

- Modified :doc:`processors/interactive` processor to change interactive template depending on the type of file path given for the thumbnail image of whole page interactives (external or internal) as well as changed the default path for the thumbnail.

0.7.2
=======================================

- Fix bug where :doc:`processors/panel` processor does not handle punctuation characters in titles and subtitles.
- Dependency updates:

  - Update ``markdown`` to 2.6.11.
  - Update ``setuptools`` to 38.4.0.
  - Update ``sphinx`` to 1.6.6.

0.7.1
=======================================

- :doc:`processors/save-title` and :doc:`processors/remove-title` processors now only search first line.

0.7.0
=======================================

- :doc:`processors/relative-link` processor will now handle query parameters.
- Modify :doc:`processors/panel` processor for translating subtitles, by requiring subtitle text as second level heading.
- Modify :doc:`processors/image` processor for translating captions, by requiring caption text between start and end tags.
- Modify :doc:`processors/image` processor to allow finer control of output, in particular when dealing with image with width values.
- Add new tag configuration value ``tag_argument`` to override tag name.
- Dependency updates:

  - Update ``markdown`` to 2.6.10.
  - Update ``Jinja2`` to 2.10.
  - Update ``setuptools`` to 38.2.5.
  - Update ``sphinx`` to 1.6.5.

0.6.1
=======================================

Fixes:

- Adds all interactives to required files.
- Typo in interactive tag documentation.

0.6.0
=======================================

Features:

- Added :doc:`processors/image-inline` processor, intended for use in tables.
- Added :doc:`processors/scratch-inline` processor for inline scratch support.

Fixes:

- Removed ``beautifulsoup4`` dependency.
- Typo in VertoResult documentation (*heading_root* -> *heading_tree*).

0.5.3
=======================================

In this hotfix Verto result data for unique identifiers and required files is now only cleared when explicitly told. Result data that is per document such as title and heading tree are cleared per conversion.

Fixes:

- Remove implicit Beautify processor, fixing white-spacing issues.
- All terms are added to glossary correctly now.

0.5.2
=======================================

Fixes:

- Verto container tags, are now supported in markdown lists.

0.5.1
=======================================

Fixes:

- Verto tags and custom tags, are now support embedding into markdown lists.

0.5.0
=======================================

Fixes:

- A new more descriptive error when an argument is given and not readable.
- Custom HTML string parsing has been implemented, allowing for correct parsing of HTML and XHTML in templates.

Documentation:

- Basic example in README.
- New contributing documentation.
- Fixed reference to incorrect file in the image processor documentation.
- Added new documentation for implicit processors.

0.4.1
=======================================

Fixes:

- pypi configuration fixes.
- pyup configuration to use develop branch.
- Improved asset file loading for deployed package.

0.4.0
=======================================

Fourth prerelease of the Verto converter.
(The project was renamed to Verto from Kordac in release.)

Adds support for the following processors:

- :doc:`processors/iframe`
- :doc:`processors/interactive`
- :doc:`processors/heading`
- :doc:`processors/scratch`
- :doc:`processors/table-of-contents`

Features:

- The :doc:`processors/scratch` processor supports ``split`` and ``random`` options.

Fixes:

- Scratch blocks work with other extensions.
- Glossary slugs are now added to the output of Verto.
- Processors are now ordered correctly.


0.3.1
=======================================

Fixes:

- Updated documentation and changelog.

0.3.0
=======================================

Third prerelease of the Verto converter.

Adds support for the following processors:

- :doc:`processors/heading`
- :doc:`processors/iframe`
- :doc:`processors/interactive`
- :doc:`processors/scratch`
- :doc:`processors/table-of-contents`

Fixes:

- Verto now orders tags correctly in the markdown pipeline.
- System tests for multiple calls to Verto and for multi-line templates.
- Glossary tags now correctly store slugs for the Verto result as per documentation.

0.2.0
=======================================

Second prerelease of the Verto converter.

Adds support for the following processors:

- :doc:`processors/button-link`
- :doc:`processors/conditional`
- :doc:`processors/glossary-link`
- :doc:`processors/video`

Adds basic support for Code Climate.

Fixes:

- Verto default processors can be accessed via a static method.
- Required and optional arguments are now explicitly matched against input.
- Made tag parameters consistently use dashes as separators.
- Tests for previous processors now explicitly test matches.
- Tests fail on docs build failures and warnings.


0.1.0
=======================================

Initial prerelease of Verto converter.

Includes the following processors:

- :doc:`processors/boxed-text`
- :doc:`processors/comment`
- :doc:`processors/image`
- :doc:`processors/panel`
- :doc:`processors/relative-link`
- :doc:`processors/remove-title`
- :doc:`processors/save-title`
