.. _command-line-mode:

Command line mode
=================

Run the tool with command line arguments, it will execute the respective
command/arguments and exit. This is helpful for automation and
scripting different test cases as part of your testing: regression,
acceptance, security etc. The way you specify the command and arguments
is the same as *interactive mode*.

Examples
--------

Run with ``help`` option:

.. code-block:: console

   $ expliot -h
   usage: expliot [-h] [cmd] ...
   
   Expliot - Internet Of Things Security Testing and Exploitation Framework
   Command Line Interface.
   
   positional arguments:
     cmd         Command to execute. If no command is given, it enters an
                 interactive console. To see the list of available commands use
                 help command
     cmd_args    Sub-command and/or (optional) arguments
   
   optional arguments:
     -h, --help  show this help message and exit

EXPLIoT commands help will provide you a list of all available commands.

.. code-block:: console

   $ expliot help
   
   Documented commands (type help <topic>):
   ========================================
   alias  exit  help  history  list  macro  quit  run  set

List all available plugins.

.. code-block:: bash

   $ expliot list
   Total plugins: 23
   
   PLUGIN                    SUMMARY
   ======                    =======
   
   ble.generic.fuzzchar      BLE Characteristic value fuzzer
   [...]
   udp.kankun.hijack         Kankun SmartPlug Hijacker

Executing a plugin
------------------

The `run` command is responsible to execute a plugin.

.. code-block:: console

   $ expliot run coap.generic.sample -h
   usage: coap.generic.sample [-h] -r RHOST [-p RPORT] [-v]
   
   Sample Description
   
   optional arguments:
     -h, --help            show this help message and exit
     -r RHOST, --rhost RHOST
                           IP address of the target
     -p RPORT, --rport RPORT
                           Port number of the target. Default is 80
     -v, --verbose         show verbose output
