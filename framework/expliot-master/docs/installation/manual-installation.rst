Manual installation
===================

The installation of ``expliot`` is straight-forward. At the moment there are
two options available. If you choose to download the archive then you are not
able to quick update to the latest version.

Requirements
------------

Make sure that your system has Python 3 available. ``expliot`` only runs with
Python 3. Also, there are a couple of other packages needed to compile various
bits and pieces.

Fedora
^^^^^^

.. code-block:: console

   $ sudo dnf -y install redhat-rpm-config libusb glib2-devel python3 python3-devel

Ubuntu (Kali Linux, Lubuntu, etc.)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt-get install git libusb-1.0 libglib2.0-dev python3 python3-dev python3-setuptools

Debian 10
^^^^^^^^^

.. code-block:: console

   $ sudo apt-get install libusb-1.0 libglib2.0-dev python3 python3-dev python3-setuptools build-essential

BlackArch
^^^^^^^^^

All requirements are shipped by default.

Alpine Linux
^^^^^^^^^^^^

It might be possible to make an installation but requires at lot of effort
because the system is using musl and ``pycrypto`` heavily depends on Glib.

Download archive
----------------

Visit the `EXPLIoT repository <https://gitlab.com/expliot_framework/expliot>`_
at GitLab and download the archive of your choice. After pressing the icon
with the cloud and the arrow you can set the archive type. After the download
unpack it.

Or use the command line:

.. code-block:: console

  $ curl -O https://gitlab.com/expliot_framework/expliot/-/archive/master/expliot-master.tar.gz
  $ tar -xzf expliot-master.tar.gz
  $ mv expliot-master expliot

Change into the ``expliot`` directory and start the installation.

.. code-block:: console

   $ cd expliot
   $ python3 setup.py install --user

Checkout from git
-----------------

The fastest way to get a copy of ``expliot`` is to clone the Git repository.

.. code-block:: console

   $ git clone https://gitlab.com/expliot_framework/expliot.git
   $ cd expliot
   $ python3 setup.py install --user

.. warning::

   If you are performing the installation as ``root``, e.g., on Kali Linux,
   then don't use ``--user``.

   .. code-block:: console

      # git clone https://gitlab.com/expliot_framework/expliot.git
      # cd expliot
      # python3 setup.py install

Troubleshooting
---------------

- On some older debian-based systems like Ubuntu and its derivatives it might
  be needed that you adjust your ``$PATH`` environment variable to include
  ``~/.local``.

- Debian-based live systems, including the latest Kali Linux, running **live**
  have some `limitations <https://gitlab.com/expliot_framework/expliot/issues/23#note_205682447>`_.
  Again, the executables in ``~/.local`` were not found. This means that you
  have to adjust your ``$PATH`` environment variable or use
  ``~/.local/bin/expliot``.

- BlackArch Linux users need to create an additional user to install
  **EXPLIoT**. Don't use ``root`` for the installation.

- If you are using Ubuntu then you need to logout and login after the
  installation.
