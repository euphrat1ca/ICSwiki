"""Test for reading data from the CAN bus."""
from binascii import hexlify
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.core.protocols.hardware.can import CanBus


# pylint: disable=bare-except
class CANRead(Test):
    """Test for reading from the CAN bus."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="readcan",
            summary="CAN bus reader",
            descr="This plugin allows you to read message(s) from the CAN bus. "
            "As of now it uses socketcan but if you want to extend it to"
            " other interfaces, just open an issue on the official"
            "expliot project repository.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=["https://en.wikipedia.org/wiki/CAN_bus"],
            category=TCategory(TCategory.CAN, TCategory.HW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-i", "--iface", default="vcan0", help="Interface to use. Default is vcan0"
        )
        self.argparser.add_argument(
            "-a",
            "--arbitid",
            type=lambda x: int(x, 0),
            help="Show messages of the specified arbitration ID only. For hex "
            "value prefix it with 0x",
        )
        self.argparser.add_argument(
            "-c",
            "--count",
            type=int,
            default=10,
            help="Specify the count of messages to read from the CANBus. Default is 10",
        )
        self.argparser.add_argument(
            "-t",
            "--timeout",
            type=float,
            help="Specify the time, in seconds, to wait for each read. Default "
            "is to wait forever. You may use float values as well i.e. 0.5",
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Reading ({}) messages from CANbus on interface({})".format(
                self.args.count, self.args.iface
            )
        )

        bus = None
        try:
            if self.args.count < 1:
                raise ValueError("Illegal count value {}".format(self.args.count))
            bus = CanBus(bustype="socketcan", channel=self.args.iface)
            for cnt in range(1, self.args.count + 1):
                message = bus.recv(timeout=self.args.timeout)
                if message is None:
                    raise TimeoutError("Timed out while waiting for CAN message")
                if self.args.arbitid:
                    if self.args.arbitid == message.arbitration_id:
                        TLog.success(
                            "(msg={})(data={})".format(
                                cnt, hexlify(message.data).decode()
                            )
                        )
                else:
                    TLog.success(
                        "(msg={})(arbitration_id=0x{:x})(data={})".format(
                            cnt, message.arbitration_id, hexlify(message.data).decode()
                        )
                    )
        except:  # noqa: E722
            self.result.exception()
        finally:
            if bus:
                bus.shutdown()
