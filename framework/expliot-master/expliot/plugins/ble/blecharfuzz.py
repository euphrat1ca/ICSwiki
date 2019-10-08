"""Support for testing BLE devices with fuzzing."""
from random import randint
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.core.protocols.radio.ble import Ble, BlePeripheral


# pylint: disable=bare-except
class BleCharFuzz(Test):
    """Test Bluetooth LE device with fuzzing."""

    def __init__(self):
        """Initialize the test."""

        super().__init__(
            name="fuzzchar",
            summary="BLE Characteristic value fuzzer",
            descr="This test allows you to fuzz the value of a characteristic "
            "and write to a BLE peripheral device. Devices that have "
            "improper input handling code for values usually crash/reboot.",
            author="Arun Magesh",
            email="arun.m@payatu.com",
            ref=["https://en.wikipedia.org/wiki/Bluetooth_Low_Energy"],
            category=TCategory(TCategory.BLE, TCategory.RD, TCategory.FUZZ),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-a",
            "--addr",
            required=True,
            help="Address of BLE device whose characteristic value will be fuzzed",
        )
        self.argparser.add_argument(
            "-n",
            "--handle",
            required=True,
            type=lambda x: int(x, 0),
            help="Specify the handle to write to. Prefix 0x if handle is hex",
        )
        self.argparser.add_argument(
            "-w",
            "--value",
            required=True,
            help="Specify the value to fuzz and write. Mark the bytes as xx in "
            "the value that you want to fuzz. For ex. if the valid value is "
            "bd0ace and you want to fuzz the 2nd byte, specify the value as "
            "bdxxce. You can also fuzz the whole value just mark all bytes as xxxxxx",
        )
        # self.argparser.add_argument("-f", "--fuzz", type=int, default=0,
        #                            help="""Specify the type of fuzzing to be performed i.e. how to change the marked
        #                                    bytes in the value. 0 = random, 1 = sequential. Default is 0""")
        self.argparser.add_argument(
            "-i",
            "--iter",
            type=int,
            default=255,
            help="Specify the no. of iterations to fuzz the value. Default is 255",
        )

        self.argparser.add_argument(
            "-r",
            "--randaddrtype",
            action="store_true",
            help="Use LE address type random. If not specified use address type public",
        )

        self.argparser.add_argument(
            "-s",
            "--noresponse",
            action="store_true",
            help="Send write command instead of write request i.e. no response, if specified",
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Fuzzing the value ({}), iterations ({}) for handle ({}) on BLE device ({})".format(
                self.args.value, self.args.iter, hex(self.args.handle), self.args.addr
            )
        )
        try:
            device = BlePeripheral()
            device.connect(
                self.args.addr,
                addrType=(
                    Ble.ADDR_TYPE_RANDOM
                    if self.args.randaddrtype
                    else Ble.ADDR_TYPE_PUBLIC
                ),
            )
            for _ in range(self.args.iter):
                value = self.args.value
                while value.find("xx") >= 0:
                    value = value.replace(
                        "xx", "{:02x}".format(randint(0, 0xFF)), 1  # nosec
                    )

                TLog.trydo("Writing the fuzzed value ({})".format(value))
                device.writeCharacteristic(
                    self.args.handle,
                    bytes.fromhex(value),
                    withResponse=(not self.args.noresponse),
                )
        except:  # noqa: E722
            self.result.exception()
        finally:
            device.disconnect()
