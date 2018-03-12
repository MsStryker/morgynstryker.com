#!/usr/bin/env python
import subprocess
from distutils.core import setup
from distutils.cmd import Command


class DocsCommand(Command):
    """Build the Sphinx docs using python setup.py docs
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        code = subprocess.call(['sphinx-build', 'docs/source', 'docs'])
        exit(code)


setup(
    name='morgynstryker',
    version='0.0.1',
    description='Morgyn Stryker Personal Website',
    author='Morgyn Stryker',
    author_email='hey@morgynstryker.com',
    url='https://github.com/MsStryker/morgynstryker.com',
    packages=[],
    cmdclass={
        'docs': DocsCommand
    }
)
