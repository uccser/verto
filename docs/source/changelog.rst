Changelog
#######################################

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
