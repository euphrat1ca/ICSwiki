Container
=========

.. warning::

   This is an ALPHA feature and not testing.

Running in a container allows one to test ``expliot`` without installation of
all dependencies locally. You have to build the image by yourself but it's
as fast as downloading it from a registry.

Requirement
-----------

Check that the ``docker` daemon is running or ``podman`` is present.

.. code-block:: console

   $ sudo systemctl start docker

``podman`` doesn't has a daemon. It's enough if the binary is installed.

Build process
-------------

Make sure that your are in the root of your ``expliot`` folder. Start the
build process for the images.

.. code-block:: console

   $ sudo docker build -t expliot -f docker/Dockerfile .

Or with ``podman``:

.. code-block:: console

   $ podman build -t expliot -f container/Dockerfile .

Consider to use ``--no-cache`` if you are teeaking the settings for your needs.

Usage
-----

Run it with ``docker``:

.. code-block:: console

   $ sudo docker run -it expliot

Or with ``podman``:

.. code-block:: console

   $ podman run -it expliot

If the container is started up you will get the prompt ``ef>``.

.. note::

   Keep in mind that there are some limitation when it comes to interacting
   with physical hardware from within a container. Thus, at the moment this
   topic is considered for advanced users only.
