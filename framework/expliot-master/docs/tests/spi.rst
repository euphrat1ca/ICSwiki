SPI
===

`Serial Peripheral Interface <https://en.wikipedia.org/wiki/Serial_Peripheral_Interface>`_
(SPI) is a synchronous, serial hardware bus communication protocol used for
intra-board (short distance) communication i.e. between two components on a
circuit board. It is a *4-wire* bus. The communication is *full-duplex* as it
has separate lines for master-to-slave and slave-to-master communication. In
many devices, you may encounter flash memory chips, for example, that talk
over SPI for data read/write and you may need a way to extract data from the
chip for further analysis or write malicious data to the chip.

spi.generic.readflash
---------------------

The current implementation is dependent on *pyspiflash* package which in
turn is dependent on *pyftdi* package. Note that there will be some extra
info printed on the console, when the plugin executes, which comes from the
*pyspiflash* package and is not part of the plugin code. To interface your PC
with the SPI flash chip, you need a hardware connector or bridge. You can use
any FTDI based device, that provides an SPI interface. We have created a
multi-protocol connector called **EXPLIoT Nano** which is available at our
`online store <https://expliot.io>`_. Although, the framework should work with
any *pyftdi* compatible FTDI device.

**Usage details:**

.. code-block:: console

    ef> run spi.generic.readflash -h

spi.generic.writeflash
----------------------

Similar considerations as `spi.generic.readflash`.

**Usage details:**

.. code-block:: console

   ef> run spi.generic.writeflash -h
