DICOM
=====

`Digital Imaging and Communications in Medicine <https://en.wikipedia.org/wiki/DICOM>`_
(DICOM) is a healthcare standard for communication and management of patient
information. It is used in various medical equipment to store and share image,
patient data, etc. If you are into medical security research the plugins will
help you in testing the security of these devices.

dicom.generic.c-echo
--------------------


This test is basically used to check if you can connect to a DICOM server and
get information about the software used as well. If you are not familiar with
DICOM, you can go through `this tutorial <http://dicomiseasy.blogspot.com/2011/10/introduction-to-dicom-chapter-1.html>`_
which explains the basics and essentials of the protocol.

**Usage details:**

.. code-block:: console

   ef> run dicom.generic.c-echo -h

Examples
^^^^^^^^

`Medical Connections <https://www.medicalconnections.co.uk/>`_ is running a
public demo `DICOM server <https://www.dicomserver.co.uk/>`_.

.. code-block:: console

   $ expliot run dicom.generic.c-echo -r www.dicomserver.co.uk -p 104
   [...]
   [*] Attempting to connect with DICOM server (www.dicomserver.co.uk) on port (104)
   [*] Using Calling AET (ANY-SCU) Called AET (ANY-SCP)
   [?] Server implementation version name (b'DicomObjects.NET')
   [?] Server implementation class UID (1.2.826.0.1.3680043.1.2.100.8.40.120.0)
   [+] C-ECHO response status (0x0000)
   [+] Test dicom.generic.c-echo Passed


dicom.generic.c-find
--------------------

This test allows you to query data from the DICOM server. The protocol does
not specify any authentication process. The authentication for C-FIND is
typically based on:

- Client IP: You can't do much about this, unless there is another way to
  extract that information or test from local network and hope there is no
  IP restriction.
- Client port: Can be specified using *-q* or *--lport* argument
- Called AET (server): Can be specified using *-s* or *--aetscp* argument

**Usage details:**

.. code-block:: console

   ef> run dicom.generic.c-find -h

Examples
^^^^^^^^

`Medical Connections <https://www.medicalconnections.co.uk/>`_ is running a
public demo `DICOM server <https://www.dicomserver.co.uk/>`_. This server can
be queried for its datasets.

.. code-block:: console

   $ expliot run dicom.generic.c-find -r www.dicomserver.co.uk -p 104
   [...]
   [*] Attempting to search for patient (*) on DICOM server (www.dicomserver.co.uk) on port (104)
   [*] Using Calling AET (ANY-SCU) Called AET (ANY-SCP) Information model (P)
   [?] Server implementation version name (b'DicomObjects.NET')
   [?] Server implementation class UID (1.2.826.0.1.3680043.1.2.100.8.40.120.0)
   [+] C-FIND query status: (0xff00)
   [+] C-FIND query Identifier: ((0008, 0005) Specific Character Set              CS: ''
   (0008, 0052) Query/Retrieve Level                CS: 'PATIENT'
   (0008, 0054) Retrieve AE Title                   AE: 'ANY-SCP'
   (0010, 0010) Patient's Name                      PN: 'ABDOMEN^VOLUNTEER^^^')
   [+] C-FIND query status: (0xff00)
   [+] C-FIND query Identifier: ((0008, 0005) Specific Character Set              CS: ''
   (0008, 0052) Query/Retrieve Level                CS: 'PATIENT'
   (0008, 0054) Retrieve AE Title                   AE: 'ANY-SCP'
   (0010, 0010) Patient's Name                      PN: 'ACEVEDO VIDARTE J F')
   [+] C-FIND query status: (0xff00)

dicom.generic.c-store
---------------------

This test allows you to store data on a DICOM server. it sends a DICOM file
to the DICOM server (SCP - Service class Provider). It can be used to test
storing wrong files of a patient or fuzzing a server.

**Usage details:**

.. code-block:: console

   ef> run dicom.generic.c-store -h

Examples
^^^^^^^^

`Medical Connections <https://www.medicalconnections.co.uk/>`_ is running a
public demo `DICOM server <https://www.dicomserver.co.uk/>`_ which should allow
the uploading of data. The sample below shows a failure.

.. code-block:: console

   $ expliot run dicom.generic.c-store -r www.dicomserver.co.uk -p 104 -f image-000000.dcm
   [...]
   [*] Attempting to send file (/home/fab/Downloads/image-000000.dcm) to DICOM server (www.dicomserver.co.uk) on port (104)
   [*] Using Calling AET (ANY-SCU) Called AET (ANY-SCP)
   [?] Server implementation version name (b'DicomObjects.NET')
   [?] Server implementation class UID (1.2.826.0.1.3680043.1.2.100.8.40.120.0)
   [-] C-STORE Failed to store file (status=0xa700)
   [-] Test dicom.generic.c-store Failed. Reason = C-STORE Failed to store file (status=0xa700)
