Documentation
=============

The documentation setup was created using Sphinx in the `docs` directory. For more information on
how to use `reStructuredText <http://www.sphinx-doc.org/en/master/rest.html>`_.

Initial Setup
-------------

This documentation was initially setup running the following command::

    (morgynstryker)$ cd docs
    (morgynstryker)$ sphinx-quickstart
    Welcome to the Sphinx 1.7.1 quickstart utility.
    ...

After entering the above command and following the prompts, a `build` directory and `Makefile` were
created.

Creating
--------

If you would like to update the documentation, you will modify the contents in the `docs/source` folder and
then run the following in the `docs` directory::

    (morgynstryker)$ make html

Viewing
-------
The documentation can be viewed locally by doing the following (in the docs directory)::

    (morgynstryker)$ open docs/build/html/index.html

