MQTT
====

`Message Queuing Telemetry Transport <https://en.wikipedia.org/wiki/MQTT>`_
(MQTT) is a messaging protocol based on publish-subscribe mechanism and works
over TCP/IP protocol stack. It is an ISO standard - `ISO/IEC 20922:2016 <https://www.iso.org/standard/69466.html>`_.
You can also read the specification `here <http://mqtt.org/documentation>`_.
It is a very famous protocol in the IoT scene and is used in various domains
from home to ICS.

mqtt.generic.crackauth
----------------------

You should use this plugin if the broker requires authentication. You can 
perform a dictionary attack on the credentials.

.. note::

   The client ID and user name are not the same.

**Usage details:**

.. code-block:: console

   ef> run mqtt.generic.crackauth -h

Examples
^^^^^^^^

For a quick check of credentials use the ``-u`` for username and ``-w`` for the
password.

.. code-block:: text

   ef> run mqtt.generic.crackauth -r 192.168.0.200 -p 1883 -u mqtt -w mqtt
   [...]
   [*] Attempting to authenticate with the MQTT Broker (192.168.0.200) on port (1883)
   [+] FOUND - (user=mqtt)(passwd=mqtt)(return code=0:Connection Accepted.)
   [+] Test mqtt.generic.crackauth Passed

To perform a real directory attack, create a text file that contains the
username/password combinations which you would like to test.

.. code-block:: text

   $ cat password-list.txt
   123456
   ha
   mqtt

.. code-block:: console

   ef> run mqtt.generic.crackauth -r 192.168.0.20 -p 1883 -u mqtt -f password-list.txt -v
   [...]
   [*] Attempting to authenticate with the MQTT broker (192.168.0.20) on port (1883)
   [*] Checking username mqtt with password 123456
   [-] Auth failed - (user=mqtt)(passwd=123456)(return code=5:Connection Refused: not authorised.)
   [*] Checking username mqtt with password ha
   [-] Auth failed - (user=mqtt)(passwd=ha)(return code=5:Connection Refused: not authorised.)
   [*] Checking username mqtt with password mqtt
   [+] FOUND - (user=mqtt)(passwd=mqtt)(return code=0:Connection Accepted.)
   [+] Test mqtt.generic.crackauth Passed

In the :ref:`Command line mode <command-line-mode>` it would be possible to
feed the username/password combinations to the input from a third-party tool.

.. code-block:: console

   $ expliot run mqtt.generic.crackauth -r 192.168.0.20 -p 1883 -u mqtt -f password-list.txt
   [...]
   [*] Attempting to authenticate with the MQTT broker (192.168.0.20) on port (1883)
   [+] FOUND - (user=mqtt)(passwd=mqtt)(return code=0:Connection Accepted.)
   [+] Test mqtt.generic.crackauth Passed

mqtt.generic.pub
----------------

During your assessment, you may want to write malicious data to a specific
topic, check if you are able to write to specific topics or corrupt ``$SYS``
topic's data. This plugin can help you with that.

**Usage details:**

.. code-block:: console

   ef> run mqtt.generic.pub -h

Examples
^^^^^^^^

Publishing a message with the payload ``running`` to the topic ``expliot`` of
a MQTT broker that requires credentials.

.. code-block:: console

   $ expliot run mqtt.generic.pub -r 192.168.0.200 -p 1883 -u admin -w 123456 -t expliot -m running
   [...]
   [*] Publishing message on topic (192.168.0.200) to MQTT Broker (expliot) on port (1883)
   [?] Using authentication (username=admin)(password=123456)
   [+] Done
   [+] Test mqtt.generic.pub Passed

mqtt.generic.sub
----------------

It is very common to check what topics we can subscribe to, what data do we
receive for further analysis or get data from ``$SYS`` topics. If you are lucky
you may end up reading sensitive data that can help you pwn the system. This
simple plugin can help you in doing that.

The default is that the connection is kept open till a message arrive. This
means that you have to press Ctrl + c if you want to stop listening.

**Usage details:**

.. code-block:: console

   ef> run mqtt.generic.sub -h

Examples
^^^^^^^^

Get two messages from `https://test.mosquitto.org/ <https://test.mosquitto.org/>`_
which are published ``/merakimv/#``.

.. code-block:: console

   ef> run mqtt.generic.sub -r test.mosquitto.org -p 1883 -t "/merakimv/#" -c 2
   [...]
   [*] Susbcribing to topic (/merakimv/#) on MQTT Broker (test.mosquitto.org) on port (1883)
   [+] (topic=/merakimv/Q2JV-J3QJ-T93R/light)(payload=b'{"lux": 11230.6}')
   [+] (topic=/merakimv/Q2JV-WBT5-MM3J/raw_detections)(payload=b'{"ts":1564219717078,...}]}')
   [+] Test mqtt.generic.sub Passed

Get the next massage from a MQTT broker that requires an username and a
password.

.. code-block:: console

   ef> run mqtt.generic.sub -r 192.168.0.200 -p 1883 -t # -u ha -w ha -c 1
   [...]
   [*] Susbcribing to topic (#) on MQTT Broker (192.168.0.200) on port (1883)
   [?] Using authentication (username=ha)(password=ha)
   [+] (topic=homeassistant/binary_sensor/e4f4/e4f4_status/config)(payload=b'{"device_class":"connectivity",...}}')
   [+] Test mqtt.generic.sub Passed
