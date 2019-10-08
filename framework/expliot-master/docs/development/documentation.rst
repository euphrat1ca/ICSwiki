Documentation
=============

The documentation is written in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
and rendered by `Sphinx <https://www.sphinx-doc.org/>`_.

The source file for are located in the ``docs`` directory and published
automatically then changes are pushed to the ``master`` branch or a merge
commit is included.

Every page contains on the top right a link called "Edit on GitLab" which
allows editing of the page without further setup.

To get started, check the `reStructuredText basics <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

Setup
-----

To create the documentation locally or if you are planing to add the
documentation of your new plugin then you need to install the generator that
is rendering the documentation.

.. code-block:: console

   $ pip3 install sphinx

Review the changes locally
--------------------------

Use ``make html`` in the ``docs`` directory to render the documentation. The
output will be available in ``_build/html``.
  
For large changes it could be useful to live-reloading documentation. 
Install the ``sphinx-reload`` Python module:

.. code-block:: console

   $ pip3 install sphinx-reload
   $ sphinx-reload docs/

The rendered content is then available at `http://localhost:5500/ <http://localhost:5500/>`_.

Create a PDF file
-----------------

It might be possible to create a PDF file but this is not supported.

.. code-block:: console

   $ make latexpdf

Commit your work
----------------

Working on the documentation is no different than to contribute code. If you
are done with your work then submit a merge request.
