Modbus
======

`Modbus <https://en.wikipedia.org/wiki/Modbus>`_ is a serial communication
protocol used in ICS (Industrial Control Systems) infrastructure, typically
be devices like PLCs etc. Modbus is still an integral part of ICS and in your
IoT assessments for Smart ICS infrastructure (Industry 4.0) you may still
encounter devices talking Modbus. 

modbus.generic.readtcp
----------------------

This plugin reads coil, register values from a Modbus server running over a
TCP/IP network. 

**Usage details:**

.. code-block:: console

   ef> run modbus.generic.readtcp -h

modbus.generic.writetcp
-----------------------

This plugin writes coil and register values to a Modbus server running over a
TCP/IP network. 

**Usage details:**

.. code-block:: console

   ef> run modbus.generic.writetcp -h
