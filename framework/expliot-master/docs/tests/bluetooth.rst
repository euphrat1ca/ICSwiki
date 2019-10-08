Bluetooth LE
============

`Bluetooth Low Energy <https://en.wikipedia.org/wiki/Bluetooth_Low_Energy>`_
(BLE) protocol is an integral part of the smart tech and used widely in home,
lifestyle, health care and enterprise IoT products.

.. note:: All plugins requires root privileges to run as of now as it needs
          scan capabilities.

ble.generic.scan
----------------

This is a generic BLE scanner to get information about BLE peripherals in the
vicinity. It performs three different operations:

1. Scan for BLE peripherals around and show their BLE addresses.
2. Enumerate and show the services of a specific  BLE peripheral (specified
   by *-a* or *--addr*)
3. Enumerate and show the characteristics of a specific  BLE peripheral
   (specified by *-a* or *--addr*)

The *-v* or *--verbose* option shows more details in the output. Some
peripherals may not connect if you have a PUBLIC addressing, in that case
it is useful to specify *-r* or *--randaddrtype*.

**Usage details:**

.. code-block:: console

   ef> run ble.generic.scan -h

**Example:**

Scan for Bluetooth LE devices with the default adapter of the system where
``expliot`` is running.

.. code-block:: console

   ef> run blescan
   [...]
   [*] Scanning BLE devices for 10 second(s)
   [+] (name=Unknown)(address=32:12:03:4d:d4:5e)
   [+] (name=Unknown)(address=b3:04:2e:de:11:fe)
   [+] Test blescan Passed

ble.generic.writechar
---------------------

This test is used to write values to a characteristic on a BLE peripheral,
provided the device lets you write data on that specific characteristic.
Which characteristic to write depends on your analysis of the available
characteristics on the BLE peripheral. You can find the characteristics and
their corresponding handle  using ``ble.generic.scan`` plugin and analyse the
BLE communication between the mobile app and the device to identify which
characteristic is used for what and what are the valid values that you can
write to it. To execute this test, you need to specify the BLE address of the
device using *-a* or *--addr* argument and the characteristic handle using
*-n* or *--handle* argument.  You may use *-s* or *--noresponse* argument if
it does not respond with a write request. The *-r* or *--randaddrtype* can be
used if the device does not respond, as described above in
``ble.generic.scan``.

**Usage details:**

.. code-block:: console

   ef> run ble.generic.writechar -h

ble.generic.fuzzchar
--------------------

This test is very interesting and the idea came to us while pentesting a
BLE device. Given, the capability to write data to characteristics, we can
also automate and fuzz the values. These semantics of these values are defined
by the developers and may be prone to memory corruption. We have tested this
on a few devices and found different results from crash, display changes to
DFU mode enable etc. Most of the arguments are the same as
``ble.generic.writechar``. The *-i* or *--iter* is the no. of iterations of
writes that you want to do and the *-w* or *--value* which is the value you
want to fuzz, you will have to replace the bytes that you want to fuzz with
*xx* and only those bytes will be randomized for each iteration.

**Usage details:**

.. code-block:: console

   ef> run ble.generic.fuzzchar -h

ble.tapplock.unlock
-------------------

This is an exploit for Tapplock, a BLE and fingerprint based door Lock. It is
a commercially available product that you can purchase from the vendor's
website or other famous e-commerce portals. The affected versions have two
different implementations for generating the auth code to unlock i.e. either
default hardcoded using *-d* or *--default* argument or generate it from the
BLE address of the lock.

**Usage details:**

.. code-block:: console

   ef> run ble.tapplock.unlock -h
