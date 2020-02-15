import setuptools
import re

with open("readme.md", "r") as fh:
    longDescription = fh.read()
    longDescription = re.sub(r'\]\(doc\/', '](https://github.com/wqking/eventpy/tree/master/doc/', longDescription)

setuptools.setup(
    name = "eventpy",
    version = "0.0.1",
    author = "wqking",
    author_email = "wqking@NOSPAMoutlook.com",
    description = "eventpy is a Python event library that provides tools that enable your application components to communicate with each other by dispatching events and listening for them. With eventpy you can easily implement signal/slot mechanism, or observer pattern.",
    long_description = longDescription,
    long_description_content_type = "text/markdown",
    url = "https://github.com/wqking/eventpy",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    platforms = ['any'],
)
