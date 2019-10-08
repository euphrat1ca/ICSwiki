"""Support for testing the storing of data on a DICOM instance."""
import os

from expliot.core.protocols.internet.dicom import (
    AE,
    StoragePresentationContexts,
    dcmread,
)
from expliot.core.tests.test import TCategory, Test, TLog, TTarget
from expliot.plugins.dicom import REFERENCE


# pylint: disable=bare-except
class CStore(Test):
    """Test the possibility to store on a DICOM instance."""

    def __init__(self):
        """Initialize the test."""

        super().__init__(
            name="c-store",
            summary="DICOM File Store",
            descr="This test case sends a C-STORE message i.e. it sends a DICOM "
            "file to the DICOM server (SCP - Service class Provider). It "
            "can be used to test storing wrong file for a patient or to "
            "fuzz test a server.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=[REFERENCE],
            category=TCategory(TCategory.DICOM, TCategory.SW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-r",
            "--rhost",
            required=True,
            help="The hostname/IP address of the target DICOM Server (SCP)",
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=104,
            type=int,
            help="The port number of the target DICOM Server (SCP). Default is 104",
        )
        self.argparser.add_argument(
            "-q",
            "--lport",
            default=0,
            type=int,
            help="If specified use this as the source/local port number",
        )
        self.argparser.add_argument(
            "-c",
            "--aetscu",
            default="ANY-SCU",
            help="Application Entity Title (AET) of Service Class User (SCU) i.e. "
            "the calling AET( client/expliot). Default is 'ANY-SCU' string.",
        )
        self.argparser.add_argument(
            "-s",
            "--aetscp",
            default="ANY-SCP",
            help="Application Entity Title (AET) of Service Class Provider (SCP) "
            "i.e. the called AET (DICOM server). Default is 'ANY-SCP' string.",
        )
        self.argparser.add_argument(
            "-f", "--file", help="Specify the DICOM file to read and send to the SCP."
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Attempting to send file ({}) to DICOM server ({}) on port ({})".format(
                self.args.file, self.args.rhost, self.args.rport
            )
        )
        TLog.generic(
            "Using Calling AET ({}) Called AET ({})".format(
                self.args.aetscu, self.args.aetscp
            )
        )
        file = None
        assoc = None
        try:
            app_entity = AE(ae_title=self.args.aetscu)
            app_entity.requested_contexts = StoragePresentationContexts
            input_file = open(self.args.file, "rb")
            dataset = dcmread(input_file, force=True)

            # 0 means assign random port in pynetdicom
            if self.args.lport != 0:
                TLog.generic("Using source port number ({})".format(self.args.lport))
                if (self.args.lport < 1024) and (os.geteuid() != 0):
                    TLog.fail("Oops! Need to run as root for privileged port")
                    raise ValueError(
                        "Using privileged port ({}) without root privileges".format(
                            self.args.lport
                        )
                    )
            assoc = app_entity.associate(
                self.args.rhost,
                self.args.rport,
                bind_address=("", self.args.lport),
                ae_title=self.args.aetscp,
            )
            TLog.trydo(
                "Server implementation version name ({})".format(
                    assoc.acceptor.implementation_version_name
                )
            )
            TLog.trydo(
                "Server implementation class UID ({})".format(
                    assoc.acceptor.implementation_class_uid
                )
            )
            if assoc.is_established:
                status = assoc.send_c_store(dataset)
                if status.Status == 0x0000:
                    TLog.success(
                        "C-STORE Success (status=0x{0:04x})".format(status.Status)
                    )
                else:
                    reason = "C-STORE Failed to store file (status=0x{0:04x})".format(
                        status.Status
                    )
                    TLog.fail(reason)
                    self.result.setstatus(passed=False, reason=reason)
            else:
                self.result.setstatus(
                    passed=False,
                    reason="Could not establish association with the server",
                )
        except:  # noqa: E722
            self.result.exception()
        finally:
            if assoc:
                assoc.release()
            if file:
                file.close()
