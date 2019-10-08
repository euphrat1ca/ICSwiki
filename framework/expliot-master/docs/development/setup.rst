Setup the development environment
=================================

If you are considering to contribute to EXPLIoT then it's recommended to use
a Python virtual environment (``venv``).

.. code-block:: console

   $ git clone https://gitlab.com/[YOUR_FORK]/expliot.git
   $ cd expliot
   $ python3 -m venv .
   $ source bin/activate
   $ python3 setup.py develop

After the basic setup it's required that you enable the pre-commit hooks for
git. Those are doing some checks and point out lint issues.

.. code-block:: console

   $ pip3 install -r requirements-dev.txt
   $ pre-commit install

To create a new feature, create a new branch in your fork.

.. code-block:: console

   $ git checkout -b new_feature master


When you are done, commit your changes and open a merge request.
