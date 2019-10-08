.. _interactive-mode:

Interactive mode
================

Run the the tool without specifying any command line arguments and you
will be greeted with a banner which shows the current version number,
name and finally the interactive console. You will now be able to run
individual plugins manually.

.. code-block:: console

   $ expliot 
   
   
                     __   __      _ _       _
                     \ \ / /     | (_)     | |
                  ___ \ V / _ __ | |_  ___ | |_
                 / _ \/   \| '_ \| | |/ _ \| __|
                 | __/ /^\ \ |_) | | | (_) | |_
                 \___\/   \/ .__/|_|_|\___/ \__|
                            | |
                            |_|
   
       
                            expliot
                       version: 0.5.0a1
                       version name: agni
   
                       Internet Of Things
                Security Testing and Exploitation
                           Framework
   
                        By Aseem Jakhar
   
               
   ef>

To see the available commands on the console type *?* or *help* and press
*Enter*.

.. code-block:: console

   ef> ?
   
   Documented commands (type help <topic>):
   ========================================
   alias  exit  help  history  list  quit  run  set  unalias


Commands
--------

As of now there are only four commands defined in the framework. The other
commands are from the ``cmd2`` module and not used for the framework. These will
be removed post beta version.

1. ``exit``: To exit from the console.
2. ``quit``: Same as ``exit``.
3. ``list``: To list down all the available plugins.
4. ``run``: To run/execute a plugin.

.. note:: All commands and plugins support tab completion. However, the plugin
          arguments, as of now, do not.

``exit`` command
----------------

As the name suggests, it is used to exit from the framework's console.
Example:

.. code-block:: console

   ef> exit

``quit`` command
----------------

It is the same as *exit* command.

Example:

.. code-block:: console

   ef> quit

``list`` command
----------------

This command lists down all the available plugins in the framework.

Example as of version 0.5.0a1:

.. code-block:: console

   ef> list
   Total plugins: 22
   
   PLUGIN                    SUMMARY
   ======                    =======

   ble.generic.fuzzchar      BLE Characteristic value fuzzer
   [...]
   udp.kankun.hijack         Kankun SmartPlug Hijacker

``run`` command
---------------

This is the main command that executes a plugin.

.. code-block:: console

   ef> run -h
   usage: run plugin
   
   Executes a plugin (test case)
   
   positional arguments:
     plugin  The test case to execute along with its options

Executing a plugin
------------------

To execute a plugin, you need to specify the plugin name and its arguments.
All the plugins are well documented and to find out their description and
arguments you need to specify the *help* argument (*-h* or *--help*) for the
plugin. We have an example plugin called *coap.generic.sample* within the
framework, which can be used to study the code for a plugin and how one can
write their own plugins. This is explained in detail in the **Development**
section. Below you can see the output of the help argument of a plugin (using
our sample plugin).

.. code-block:: console

   ef> run coap.generic.sample -h
   usage: coap.generic.sample [-h] -r RHOST [-p RPORT] [-v]

   Sample Description

   optional arguments:
     -h, --help            show this help message and exit
     -r RHOST, --rhost RHOST
                           IP address of the target
     -p RPORT, --rport RPORT
                           Port number of the target. Default is 80
     -v, --verbose         show verbose output

Output of the BLE scanner plugin help argument:

.. code-block:: console

   ef> run ble.generic.scan -h
   usage: ble.generic.scan [-h] [-i IFACE] [-t TIMEOUT] [-a ADDR] [-r] [-s] [-c]
                           [-v]
   
   This test allows you to scan and list the BLE devices in the proximity. It can
   also enumerate the characteristics of a single device if specified. NOTE: This
   plugin needs root privileges. You may run it as $ sudo expliot
   
   optional arguments:
     -h, --help            show this help message and exit
     -i IFACE, --iface IFACE
                            HCI interface no. to use for scanning. 0 = hci0, 1 =
                            hci1 and so on. Default is 0
     -t TIMEOUT, --timeout TIMEOUT
                        Scan timeout. Default is 10 seconds
     -a ADDR, --addr ADDR  Address of BLE device whose services/characteristics
                           will be enumerated. If not specified, it does an
                           address scan for all devices
     -r, --randaddrtype    Use LE address type random. If not specified use
                           address type public
     -s, --services        Enumerate the services of the BLE device
     -c, --chars           Enumerate the characteristics of the BLE device
     -v, --verbose         Verbose output. Use it for more info about the devices
                           and their characteristics
