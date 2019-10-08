Development
===========

This section contains details about the structure of EXPLIoT.

Bin
---

**Module Directory**: ``bin``

This module contains the executable scripts for the framework.

expliot
~~~~~~~

This script starts the console for the user. It just initializes the
`Cli`_ class as explained in the `ui`_ section below. The components
of the script are:

#. ``class EfCli()`` - It is responsible for running the Cli.

   #. Methods:

      #. ``main(cls)`` - Class method that starts the command loop.

   #. Members:

      #. ``banner`` - The EXPLIoT intro banner
      #. ``cli`` - Object of the `Cli`_ class`

.. _expliot: https://gitlab.com/expliot_framework/expliot/tree/master/bin/expliot
.. _Cli: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/ui/cli/__init__.py

Core
----

**Module Directory**: ``expliot/core``

The core of the framework provides all the functionality and object
definitions required by the plugins. It contains all the modules that
make up the framework.

Common
~~~~~~

**Module Directory**: ``expliot/core/common``

This module contains the common utility methods and classes that perform
generic/common tasks. As of now there is not much functionality in this
module. Going forward all generic/repeated tasks will be added here. The
current packages include:

1. ``exceptions.py`` - All framework specific exceptions will go here.

   1. ``sysexcinfo()`` - Used by plugins for logging any internal
      exception that is not specifically handled by the plugin itself.

2. ``fileutils.py`` - All file based utility methods will go here.

   1. ``readlines_both(file1, file2)`` - Unused as of now. This method
      reads two files and yields each line from the second file for each
      line in the first file. Good for user and password
      enumeration/dictionary.


Interfaces
~~~~~~~~~~

**Module Directory**: ``expliot/core/interfaces``

These are interface modules for any external hardware connected to the
system. This can be utilized internally by protocols module for
interfacing and communicating with the hardware.

ftdi
^^^^

**Module Directory**: ``expliot/core/interfaces/ftdi``

This module is an interface for any `Future Technology Devices
International(FTDI)`_ device connected to the system. It is a wrapper
over *pyspiflash* and *pyi2cflash* which internally depend on the
*pyftdi* package. Currently, it is utilized by *protocols.hardware.spi*
and *protocols.hardware.i2c* modules.

``__init__.py`` - The wrapper implementation for the interface. The
details of classes and methods are given below.

1. ``class SpiFlashManager(SerialFlashManager)`` - A wrapper over
   *pyspiflash SerialFlashManager*. More details can be found at
   `https://github.com/eblot/pyspiflash`_

   1. ``close(device)`` - Static method. Calls terminate() on
      SpiController (in *pyspiflash*) to release the resource.

2. ``class I2cEepromManager(SerialEepromManager)`` - A wrapper over
   *pyi2cflash SerialEepromManager*. More details can be found at
   `https://github.com/eblot/pyi2cflash`_

   1. ``close(device)`` - Calls terminate() on the *I2cController* (in
      *pyi2cflash*) to release the resource.

.. _Future Technology Devices International(FTDI): https://en.wikipedia.org/wiki/FTDI
.. _`https://github.com/eblot/pyspiflash`: https://github.com/eblot/pyspiflash
.. _`https://github.com/eblot/pyi2cflash`: https://github.com/eblot/pyi2cflash

Protocols
~~~~~~~~~

**Module Directory**: ``expliot/core/protocols``

This module is the home for all the different protocol implementations.
All plugins are strictly required to import protocol specific
functionality from here and not import from any other package outside of
the framework. The protocols are grouped into submodules based on their
usage and implementation:

#. *protocols.hardware* - Home for all hardware specific protocols
#. *protocols.internet* - Home for all TCP/IP based protocols
#. *protocols.radio* - Home for all radio specific protocols

.. note::

   As per the unified Interface mentioned above, even
   though an EXPLIoT dependency package is installed, DO NOT import it in
   your plugins. All protocol imports *must* be from this module.

protocols.hardware
^^^^^^^^^^^^^^^^^^

**Module Directory**: ``expliot/core/protocols/hardware``

All the hardware based protocol implementations go inside this module.

CAN
'''

**Module Directory**: ``expliot/core/protocols/hardware/can``

The CAN implementation, currently, is a wrapper over *python-can*
package.

``__init__.py`` - The CAN wrapper implementation over *python-can*. The
details of classes, methods etc. are given below.

#. ``class CanBus(Bus)`` - Wrapper over *python-can* Bus class.
#. ``class CanMessage(Message)`` - Wrapper over *python-can* Message
   class.

.. note::

   If any other python-can class, method etc. is required for a
   plugin, it must be added here.

I2C
'''

**Module Directory**: ``expliot/core/protocols/hardware/i2c``

The I2C implementation, currently, is a wrapper over *pyi2cflash*
package. The details of classes, methods etc. are given below.

#. ``__init__.py`` - It just imports *I2cEepromManager* class from
   *expliot.core.interfaces.ftdi* module, which can be used to interact
   with an FTDI device for I2C communication.

.. note::

   If any other pyi2cflash class, method etc. is required for a
   plugin, it must be added in `expliot.core.interfaces.ftdi`` and then
   imported in to this module.

serial
''''''

**Module Directory**: ``expliot/core/protocols/hardware/serial``

The serial implementation, currently, is a wrapper over *pyserial*
package. The details of classes, methods etc. are given below.

#. ``__init__.py`` - The serial wrapper implementation over *pyserial*.
   The details of classes, methods etc. are given below.

   #. ``class Serial(Pserial)`` - Wrapper over *pyserial* Serial class

      #. ``readfull(self, bsize=1)`` - reads *bsize* bytes of data from
         the serial connection.

.. note::

   If any other pyserial class, method etc. is required for a
   plugin, it must be added here.


SPI
'''

**Module Directory**: ``expliot/core/protocols/hardware/spi``

The SPI implementation, currently, is a wrapper over *pyspiflash*
package. The details of classes, methods etc. are given below.

#. ``__init__.py`` - It just imports *SpiFlashManager* class from
   *expliot.core.interfaces.ftdi* module, which can be used to interact
   with an FTDI device for SPI communication.

.. note::

   If any other pyspiflash class, method etc. is required for a
   plugin, it must be added in expliot.core.interfaces.ftdi and then
   imported in to this module.**

protocols.internet
^^^^^^^^^^^^^^^^^^

**Module Directory**: ``expliot/core/protocols/internet``

All the TCP/IP network based protocol implementations go inside this
module.

COAP
''''

**Module Directory**: ``expliot/core/protocols/internet/coap``

It is not implemented yet but will be added soon.

DICOM
'''''

**Module Directory**: ``expliot/core/protocols/internet/dicom``

The DICOM implementation, currently, is a wrapper over *pynetdicom*
package.

#. ``__init__.py`` - The DICOM wrapper implementation over *pynetdicom*.
   The details of classes, methods etc. are given below.

   #. ``class AE(AppEntity)`` - Wrapper over *pynetdicom* AE class.
   #. ``class Dataset(DS)`` - Wrapper over *pynetdicom* Dataset class.
   #. Constants/variables Imported -
      ``VerificationPresentationContexts, QueryRetrievePresentationContexts, BasicWorklistManagementPresentationContexts``

.. note::

   If any other pynetdicom class, method etc. is required for a
   plugin, it must be added here.



Modbus
''''''

**Module Directory**: ``expliot/core/protocols/internet/modbus``

The Modbus implementation, currently, is a wrapper over *pymodbus*
package. Currently, Modbus over TCP is supported. The other
communication methods will be supported soon.

#. ``__init__.py`` - The Modbus wrapper implementation over *pymodbus*.
   The details of classes, methods etc. are given below.

   #. ``class ModbusTcpClient(MBTClient)`` - Wrapper over *pymodbus*
      ModbusTcpClient class.

.. note::

   If any other pymodbus class, method etc. is required for a
   plugin, it must be added here.

MQTT
''''

**Module Directory**: ``expliot/core/protocols/internet/mqtt``

The MQTT implementation, currently, is a wrapper over *paho-mqtt*
package. Currently, MQTT directly over TCP is supported. The other
communication methods will be supported soon.

#. ``__init__.py`` - The MQTT wrapper implementation over *paho-mqtt*.
   The details of classes, methods etc. are given below.

   #. ``class SimpleMqttClient()`` - A simple client that implements
      basic mqtt communication methods.

      #. ``pub(topic, **kwargs)`` - Static method. Wrapper over
         *paho-mqtt subscribe.simple()* method.
      #. ``pub(topic, **kwargs)`` - Static method. Wrapper over
         *paho-mqtt publish.single()* method.
      #. ``pubmultiple(msgs, **kwargs)`` - Static method. Wrapper over
         *paho-mqtt publish.multiple()* method.
      #. ``connauth(host, clientid=None, user=None, passwd=None, **kw)``
         - Checks if a client can connect to a broker with specific
         client id and/or credentials.

   #. ``class MqttClient(Client)`` - Wrapper over *paho-mqtt* Client
      class.

.. note::

   If any other paho-mqtt class, method etc. is required for a
   plugin, it must be added here.

protocols.radio
^^^^^^^^^^^^^^^

**Module Directory**: ``expliot/core/protocols/radio``

All the radio based protocol implementations go inside this module.

BLE
'''

**Module Directory**: ``expliot/core/protocols/radio/ble``

The BLE implementation, currently, is a wrapper over *bluepy* package.

#. ``__init__.py`` - The BLE wrapper implementation over *bluepy*. The
details of classes, methods etc. are given below.

   #. ``class BleScanner(btle.Scanner)`` - Wrapper over *bluepy* Scanner class.
   #. ``class BlePeripheral(btle.Peripheral)`` - Wrapper over *bluepy* Peripheral class.
   #. ``class Ble()`` - Implements the scan logic.

#. ``scan(iface=0, tout=10)`` - Scans on a given BLE interface for a specified amount of time.

.. note::

   If any other bluepy class, method etc. is required for a plugin,
   it must be added here.

tests
~~~~~

All the test case related implementation like base test case classes,
plugin management etc. goes here.

`test.py`_
^^^^^^^^^^

This file has the interface definition for a test case. The plugins
inherit from this base class. The details of classes, methods etc. are
given below.

#. ``class TCategory(namedtuple("TCategory", "proto, iface, action"))``
   - This class provides the definition for the category of a test case
   (plugin) which includes the protocol used, interface and action. For
   details refer the code documentation.
#. ``class TTarget(namedtuple("TTarget", "name, version, vendor"))`` -
   This class defines the target of the test case (plugin). The plugins
   can be generic or specific to an IoT product.
#. ``class TResult()`` - This class holds the status of a test case
   (plugin) i.e. fail, pass and the reason for failure.

   #. ``setstatus(self, passed=True, reason=None)`` - method used to set
      the status of a test.
   #. ``exception(self)`` - Set the failure status using the exception
      information as the reason.

#. ``class TLog()`` - Logger class that must be used by the plugins for
   logging any output. Plugins must not use any other print methods. You
   do not need to instantiate it, but just call *init()* to specify the
   output destination.

   #. ``init(cls, file=None)`` - Class method. Used to initialize the
      log to a file or *stdout*
   #. ``close(cls)`` - Class method. Close the file object if not
      *stdout*
   #. ``success(cls, msg)`` - Class method. Prints the *msg* with
      success ("*[+]*") prefix.
   #. ``fail(cls, msg)`` - Class method. Prints the *msg* with fail
      ("*[-]*") prefix.
   #. ``trydo(cls, msg)`` - Class method. Prints the *msg* with try
      ("*[?]*") prefix.
   #. ``generic(cls, msg)`` - Class method. Prints the *msg* with
      generic ("*[*]*") prefix.

#. ``class Test`` - The base class for a test case. The plugin **must**
   inherit from this class. It defines the basic functionality for
   defining and executing a plugin.

   #. **Methods:**

      #. ``__init__(self, **kwargs)`` - Plugin description
         initialization.
      #. ``execute(self)`` - The main plugin execution method. It is
         **mandatory** for the plugin to override this method.
      #. ``pre(self)`` - Any setup dependency logic for the plugin needs
         to be implemented here. It is optional for the plugin to
         override this method. Please **do not** implement argument
         parsing logic here, that needs to go in *execute()* method. As
         of now this method is not used by any plugins.
      #. ``post(self)`` - Any cleanup logic for the plugin needs to be
         implemented here. It is optional for the plugin to override
         this method. Please **do not** implement any success/fail logic
         here, that needs to go in *execute()* method.
      #. ``intro(self)`` - Prints plugin information when executed. Used
         internally for output. Plugin **must not** override this
         method.
      #. ``run(self, arglist)`` - Executes the
         ``pre(), post(), execute()``

.. _test.py: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/tests/test.py


`testsuite.py`_
^^^^^^^^^^^^^^^

This file implements the collection to manage the plugins. This is used
by both ``list`` and ``run`` commands.

#. ``class TestSuite(dict)`` - This class basically imports all the
   plugin classes holds all the plugin IDs. It is instantiated by the
   ``Cli`` object and used for loading and executing the plugin
   requested by the user.

   #. ``__init__(self, pkgname='expliot.plugins')`` - Loads all the
      plugins. It internally calls ``import_plugins()`` to do the dirty
      work.
   #. ``import_plugins(self, pkgname)``- Imports the plugins recursively
      from ``pkgname`` package.

ui
~~

**Module Directory**: ``expliot/core/ui``

This is the home for all the different user interface implementations
for the framework. As of now, we just have a command line interface for
the framework.

.. _testsuite.py: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/tests/testsuite.py


cli
^^^

**Module Directory**: ``expliot/core/ui/cli``

This module is currently built with the `cmd2`_ Python package for
creating and managing the Command line interface.

Refer the code in `expliot/core/ui/cli/\ init.py`_ for more details.

This file has the code for the CLI as of now.

#. ``class Cli(Cmd)`` - The main class that implements the `cmd2`_
   CLI logic. It loads all the plugins using the ``tsuite`` member
   object of class `TestSuite`_.

   #. ``__init__(self, prompt=None, intro=None)`` - The constructor of
      the class. This is used for initializing *cmd2* members.
   #. ``del_defaultcmds(self)`` - This method removes the `cmd2`_
      default commands that come along with it as we do not want to show
      it in `expliot`_.
   #. ``do_list(self, args)`` - This callback method implements the
      ``list`` command in ``expliot``.
   #. ``do_run(self, arglist)`` - The callback method implements the
      ``run`` command in ``expliot``.
   #. ``complete_run(self, text, line, start_index, end_index)`` - This
      callback method implement the TAB completion of plugin names in
      the ``run`` command.
   #. ``runtest(self, name, arglist)`` - This method is internally
      called by ``do_run()`` and calls the ``run()`` method of the
      plugin object.
   #. ``Cmd.do_exit`` - This is an alias defined for ``Cmd.do_quit``
      method provided by default in `cmd2`_

Adding a new command
''''''''''''''''''''

To add a new command, we need to implement a callback method in the
`Cli`_ class as we have done for ``run`` and ``list`` commands. As
per `cmd2`_ documentation` to add a new command, you need to
implement a callback method in your code and the method name should be
of the format ``do_commandname()``. For example, to add a command
``foobar`` we will implement a callback method ``do_foobar()``.

.. _cmd2: https://cmd2.readthedocs.io/en/latest/
.. _expliot/core/ui/cli/\ init.py: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/ui/cli/__init__.py
.. _TestSuite: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/tests/testsuite.py
.. _Cli: https://gitlab.com/expliot_framework/expliot/tree/master/expliot/core/ui/cli/__init__.py
