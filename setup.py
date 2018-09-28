from setuptools import setup, find_packages
import sys
from verto import __version__

if not sys.version_info[0] == 3:
    sys.exit('Sorry, currently only Python 3 is supported.')

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='verto',
    version=__version__,
    description='Verto is an extension of the Python Markdown package, which allows authors to include complex HTML elements with simple text tags in their Markdown.',
    long_description=long_description,
    url='https://github.com/uccser/verto',
    author='University of Canterbury Computer Science Education Research Group',
    author_email='csse-education-research@canterbury.ac.nz',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    keywords='markdown verto development textbook converter media richtext interactive education html book author extension',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
