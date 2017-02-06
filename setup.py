from setuptools import setup, find_packages

setup(
    name='kordac',
    version='0.0.2',
    description='Kordac is an extension of the Python Markdown package, which allows authors to include complex HTML elements with simple text tags in their Markdown files.',
    url='https://github.com/uccser/kordac',
    author='UCCSER',
    author_email='jack.morgan@canterbury.ac.nz',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'markdown>=2.6.8',
        'python-markdown-math>=0.2'
    ],
    zip_safe=False
)
