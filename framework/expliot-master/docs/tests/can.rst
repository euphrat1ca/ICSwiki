CAN
===

`Controller Area Network <https://en.wikipedia.org/wiki/CAN_bus>`_ (or CAN Bus)
is a robust hardware communication protocol primarily used in vehicles. Other
noted uses are in Industrial automation, Building automation, elevators etc.
CAN hacking has really caught up due to advancements in automotive technology
or in business terms introduction of IoT in automotive. Hence, it makes sense
to have test case for security researchers to be able to analyse CAN enabled
devices.

It uses `socketscan`_ as of now. You need to have a physical CAN interface on
your system which is connected to the CANBus or for testing you can use a
simulator and `socketscan`_ as a virtual can interface.

can.generic.readcan
-------------------

This test reads and shows the data on the CANBus.

**Usage details**

.. code-block:: console

   ef> run can.generic.readcan -h

can.generic.writecan
--------------------

This test writes data on the CANBus.

**Usage details**

.. code-block:: console

   ef> run can.generic.writecan -h

.. _socketscan: https://en.wikipedia.org/wiki/SocketCAN