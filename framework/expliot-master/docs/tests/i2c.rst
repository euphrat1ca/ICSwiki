I2C
===

`Inter-Integrated Circuit <https://en.wikipedia.org/wiki/I%C2%B2C>`_ (I2C) is a
synchronous, serial hardware bus communication protocol used for intra-board
(short distance) communication i.e. between two components on a circuit board.
It is a *2-wire* bus. It is also used in EEPROMs for example to read and write
data.

i2c.generic.readeeprom
----------------------

The current implementation is dependent on *pyi2cflash* package which in turn
is dependent on *pyftdi* package. Note that there will be some extra info
printed on the console, when the plugin executes, which comes from the
*pyi2cflash* package and is not part of the plugin code. To interface your
PC with the I2C EEPROM chip, you need a hardware connector or bridge. You can
use any FTDI based device, that provides an I2C interface. We have created a
multi-protocol connector called **EXPLIoT Nano** which is available at our
`online store <https://expliot.io>`_. Although, the framework should work with
any *pyftdi* compatible FTDI device.

**Usage details:**

.. code-block:: console

   ef> run i2c.generic.readeeprom -h

i2c.generic.writeeeprom
-----------------------

Similar considerations as ``i2c.generic.readeeprom``.

**Usage details:**

.. code-block:: console

   ef> run i2c.generic.writeeeprom -h
