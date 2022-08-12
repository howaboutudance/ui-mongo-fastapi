# Python Template Project

A template for creating python project using:
- tox
- pytest
- mypy
- setuptool
- gnu make

# Setup:

As a template, this provides a series of files that needed to be modified:
- setup.py
- Makefile
- Dockerfile
- tox.ini

```TODO``` comments have been added for required sections to edit.

Optionally, this repo is by default licensed Apache 2.0 and will want to replace LICENSE with the apporpriate text if different.


## setup.py
This file is used by tox and defines a package (for setuptools). In the call to
setuptools.setup you need to modify:

- name -- with the name of your package (should be pypi compatible)
- author and author_email -- contacts for the developer
- description -- the a description of the package
- urls and project_urls { Bug Tracker } -- links to the repo and it's bug tracker


## Makefile
The Makefile assumes you will being build a package/library names ```sample_module``` that will execute a function ```sample.helloworld```. You will want to:

- modify local-test have ```mypy`` check another folder besides sample_module

## Dockerfile.sample

The Dockerfile is a sample if you would like to run a application utilizing the wheel/setuptools package toolset to build small containers, use pytest to run tests inside a container and provide a ipython console if you want to troubleshoot inside a container environment.

It makes a few assumptions:
- run ``__main__.py`` of ``sample_module`` in the execution repo
- copy in the egg matching the nam  sample_module (line 28)

These need to be changes to reflect change made to ```setup.py``` and your package structure.


# Development Environment:

To start a virtualenv that matches the packages utilized to develop the package:

```bash
make init-env
```

This will create a new folder holding the virtualenv ```venv<major-version>```
and install packages from requirements.txt and requirements-dev.txt