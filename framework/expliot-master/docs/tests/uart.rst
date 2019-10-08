UART
====

`Universal Asynchronous Receiver/Transmitter <https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter>`_ (UART)
is not a hardware bus protocol, but a physical circuit that is used for
serial communication between two components. The speed (baud rate) and data
format are configurable, as the communication is asynchronous. UART is one
of the most famous mechanisms for devices to have an interface with the
outside world. Typically, a shell or a console runs over the UART port, so
developers, support staff can access the running device for troubleshooting,
etc. It is a very interesting opportunity, from a security perspective, to
gain access to a UART port and be able to interact with a console or read
data on the connection.

uart.generic.baudscan
---------------------

Since, the communication is asynchronous, the baud rate/format must be pre-
configured for the two UART devices to talk to each other. There are some
well-known baud rates that are usually used. However, if you don't know the
correct baud rate for communication, you will end up with garbage data due to
a mismatch on baud rate at both the ends. Hence, to analyse a UART port, we
still need to know the correct baud rate of the device. This plugin just
enumerates over different baud rates and analyses the received data for valid
ASCII characters to identify the correct baud rate of the UART port on the
device. You will need a USB UART converter to enable your PC to talk to the
device UART port. There are many connectors available in the market. We have
created a multi-protocol (including UART) connector called **EXPLIoT Nano**
which is available at our `online store <https://expliot.io>`_.
Although, the
framework should work with any *Linux* compatible USB-UART connector (also
called USB-TTL).

**Usage details:**

.. code-block:: console

   ef> run uart.generic.baudscan -h

Examples
^^^^^^^^

For an ESP32 device connected to ``/dev/ttyUSB3`` the output could look like
in the following sample.

.. code-block:: text

  ef> run uart.generic.baudscan -p /dev/ttyUSB3
  [...]
  [*] Connecting to the the serial port (/dev/ttyUSB3) timeout (3)
  [*] Scanning for baud rates: 1200,2400,4800,9600,19200,38400,57600,115200
  [+] Checking baud rate: 1200
  [+] 	ASCII ratio: 0/4, 0.0 %
  [+] Checking baud rate: 2400
  [-] 	No data received
  [+] Checking baud rate: 4800
  [+] 	ASCII ratio: 2/13, 15.38 %
  [+] Checking baud rate: 9600
  [-] 	No data received
  [+] Checking baud rate: 19200
  [-] 	No data received
  [+] Checking baud rate: 38400
  [+] 	ASCII ratio: 13/30, 43.33 %
  [+] Checking baud rate: 57600
  [+] 	ASCII ratio: 8/30, 26.67 %
  [+] Checking baud rate: 115200
  [-] 	No data received
  [*] Baud rate 38400 has max. ASCII percentage of 43.33 %
  [-] Test uart.generic.baudscan Failed. Reason = No good baud rate found

uart.generic.fuzzcmds
---------------------

When the devices have a custom console running on a UART port, this plugin
can help you in identifying undocumented or hidden console commands as well
as fuzz commands and their arguments. We have been able to crash as well as
find hidden commands using the same technique. The basic idea behind this
plugin is that the console with respond with different output for valid and
invalid commands or their parameters and given the knowledge of a valid
output you can fuzz/brute-force the commands. It allows you to specify a
character set  (*-c* or *--chars* argument) and length (*-l* or *--length*)
to generate random strings which it sends to the device and analyses the
response. You can also specify a match criteria string (*-m* or *--match*)
which means that it will be considered as a valid response if the response
contains this string. Alternatively, you can also specify a no-match criteria
string (*-n* or *--nomatch*) which will tell the plugin to ignore the response
and treat it as invalid if the response contains this string. To fuzz specific
parts of the commands string you can specify a prefix string (*-x* or
*--prefix*) and an append string (*-a* or *--append*) which are prefixed and
appended to the generated fuzz string and then sent to the device UART. You
may need to toggle and play around with *-t* or *--timeout* and *-z* or
*--buffsize* arguments for optimum speed execution and then use the best
values for the final fuzzing. Note that printing on the terminal will make
the execution slow, so avoid *-v* or *--verbose* option for the final
execution. The *-v* option comes handy when you just start analyzing the
responses.

**Usage details:**

.. code-block:: console

   ef> run uart.generic.fuzzcmds -h

Example
-------

To try this ``uart.generic.fuzzcmds``, upload the code below to an Arduino or
a compatible device.

.. code-block:: c

   const int ledPin = LED_BUILTIN;
   int incomingByte;

   void setup() {
     Serial.begin(115200);
     pinMode(ledPin, OUTPUT);
   }

   void loop() {
     // Check if there is serial data available
     if (Serial.available() > 0) {
       // Read the oldest byte in the serial buffer
       incomingByte = Serial.read();
       // A h will turn the LED on and a l off
       if (incomingByte == 'h') {
         digitalWrite(ledPin, HIGH);
         Serial.write("Hit");
       } else if (incomingByte == 'l') {
         digitalWrite(ledPin, LOW);
         Serial.write("Hit");
       }
     }
   }


``uart.generic.fuzzcmds`` will try with a given alphabet to trigger responses.

.. code-block:: console

   ef> run uart.generic.fuzzcmds -p /dev/ttyACM0 -l 1 -m Hit
   [...]
   [*] Connecting to the the serial port (/dev/ttyACM0) with baud (115200)
   [*] Using chars(abcdefghijklmnopqrstuvwxyz) and length(1)
   [+] Command=(h) found. --match criteria in Response=(b'Hit')
   [+] Command=(l) found. --match criteria in Response=(b'Hit')
   [*] Tried 20 commands till now
   [+] Valid Commands found: (['h', 'l'])
   [+] Test uart.generic.fuzzcmds Passed
