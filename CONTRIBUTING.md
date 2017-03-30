# Contributing Guide

Welcome to the Verto developer community! We have spent many months developing this project, and we would love for you to get involved!

We've written a technical guide about how Verto works and how to contribute [here](verto.readthedocs.io/en/develop/contributing.html). These docs should give you a good overview of how Verto is pieced together.

Below are a few more general notes to remember while you are working on Verto.

### Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [csse-education-research@canterbury.ac.nz](mailto:csse-education-research@canterbury.ac.nz)

### Reporting issues

This section guides you through submitting an issue for Verto.
Following these guidelines helps maintainers and the community understand your findings.

Before submitting an issue, please take a look at the [issues](https://github.com/uccser/verto/issues) on the repository to check it hasn't already been reported.

### Your first code contribution

Unsure where to begin contributing to Verto? Take a look at the [issues](https://github.com/uccser/verto/issues) on the repository.

### Pull requests

- Include a detailed explaination of the proposed change
- Read and applied the [style guides listed below](#style-guides).
- Your pull request should be on a new branch from our `develop` branch (unless it's something tiny like a typo). The naming conventions of branches should be descriptive of the new addition/modification. Ideally they would specify their namespace as well, for example:
  - `processor/image`
  - `issue/234`
- Linked any relevant [existing issues](https://github.com/uccser/verto/issues).
- Run the test suite and all tests passed
- Added necessary documentation (if appropriate).

## Style guides

### Git

- Commits should be as descriptive as possible. Other developers (and even future you) will thank you for your forethought and verbosity for well documented commits. [Ideally follow this commit structure](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html), otherwise in short:
  - Limit the first line to 72 characters or less
  - Reference issues and pull requests liberally
- Use [Vincent Driessen's Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/) for managing development. Please read this document to understand our branching methods.

### Programming

> Every line of code should appear to be written by a single person, no matter the number of contributors.

These are our abridged guidelines for working on code within this repository:
- Code should be easily readable (avoid abbreviations etc)
- Files should be set to `utf-8`, use `lf` line endings, and have a final newline at the end of a file.
- Functions should have comments/docstrings explaining their purpose.
- Indents should be spaces (not tab characters)
- Indent sizes:
  - HTML: 2 spaces
  - Python: 4 spaces

We aim to follow the [PEP8 style guide](https://www.python.org/dev/pep-0008/) and use [Flake8](flake8.pycqa.org/en/latest/) to enforce this.
