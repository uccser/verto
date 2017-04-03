Changelog
#######################################

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
