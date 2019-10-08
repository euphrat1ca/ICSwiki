"""Support to scan for BLE devices."""
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.core.common.exceptions import sysexcinfo
from expliot.core.protocols.radio.ble import Ble, BlePeripheral


# pylint: disable=bare-except, too-many-nested-blocks
class BleScan(Test):
    """Scan for BLE devices."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="scan",
            summary="BLE Scanner",
            descr="This test allows you to scan and list the BLE devices in "
            "the proximity. It can also enumerate the characteristics "
            "of a single device if specified. NOTE: This plugin needs "
            "root privileges. You may run it as $ sudo expliot.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=["https://en.wikipedia.org/wiki/Bluetooth_Low_Energy"],
            category=TCategory(TCategory.BLE, TCategory.RD, TCategory.RECON),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
            needroot=True,
        )

        self.argparser.add_argument(
            "-i",
            "--iface",
            default=0,
            type=int,
            help="HCI interface no. to use for scanning. 0 = hci0, 1 = hci1 "
            "and so on. Default is 0",
        )
        self.argparser.add_argument(
            "-t",
            "--timeout",
            default=10,
            type=int,
            help="Scan timeout. Default is 10 seconds",
        )
        self.argparser.add_argument(
            "-a",
            "--addr",
            help="Address of BLE device whose services/characteristics will "
            "be enumerated. If not specified, it does an address scan for all devices",
        )
        self.argparser.add_argument(
            "-r",
            "--randaddrtype",
            action="store_true",
            help="Use LE address type random. If not specified use address type public",
        )
        self.argparser.add_argument(
            "-s",
            "--services",
            action="store_true",
            help="Enumerate the services of the BLE device",
        )
        self.argparser.add_argument(
            "-c",
            "--chars",
            action="store_true",
            help="Enumerate the characteristics of the BLE device",
        )
        self.argparser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Verbose output. Use it for more info about the devices and "
            "their characteristics",
        )
        self.found = False
        self.reason = None

    def execute(self):
        """Execute the test."""
        if self.args.addr is not None:
            self.enumerate()
        else:
            self.scan()
        self.result.setstatus(passed=self.found, reason=self.reason)

    def scan(self):
        """
        Scan for BLE devices in the proximity.

        :return:
        """
        TLog.generic("Scanning BLE devices for {} second(s)".format(self.args.timeout))
        try:
            devices = Ble.scan(iface=self.args.iface, tout=self.args.timeout)
            for device in devices:
                self.found = True
                TLog.success(
                    "(name={})(address={})".format(
                        device.getValueText(Ble.ADTYPE_NAME) or "Unknown", device.addr
                    )
                )
                if self.args.verbose is True:
                    TLog.success("    (rssi={}dB)".format(device.rssi))
                    TLog.success("    (connectable={})".format(device.connectable))
                    for scan_data in device.getScanData():
                        TLog.success("    ({}={})".format(scan_data[1], scan_data[2]))
        except:  # noqa: E722
            self.reason = "Exception caught: {}".format(sysexcinfo())

        if self.found is False and self.reason is None:
            self.reason = "No BLE devices found"

    def enumerate(self):
        """
        Enumerate the services and/or characteristics of the specified BLE device.

        :return:
        """
        # Documentation is wrong, the first keyword argument is deviceAddr instead of
        # deviceAddress. http://ianharvey.github.io/bluepy-doc/
        if self.args.services is False and self.args.chars is False:
            TLog.fail(
                "Specify the enumerations option(s). Either or both - services, chars"
            )
            self.reason = "Incomplete arguments"
            return

        TLog.generic(
            "Enumerating services/characteristics of the device {}".format(
                self.args.addr
            )
        )
        device = BlePeripheral()
        try:
            device.connect(
                self.args.addr,
                addrType=(
                    Ble.ADDR_TYPE_RANDOM
                    if self.args.randaddrtype
                    else Ble.ADDR_TYPE_PUBLIC
                ),
            )
            self.found = True
            if self.args.services is True:
                services = device.getServices()
                for service in services:
                    TLog.success(
                        "(service uuid={})(handlestart={})(handleend={})".format(
                            service.uuid, hex(service.hndStart), hex(service.hndEnd)
                        )
                    )
            if self.args.chars is True:
                chars = device.getCharacteristics()
                for char in chars:
                    TLog.success(
                        "(characteristic uuid={})(handle={})".format(
                            char.uuid, hex(char.getHandle())
                        )
                    )
                    if self.args.verbose is True:
                        support_read = char.supportsRead()
                        TLog.success("    (supports_read={})".format(support_read))
                        if support_read is True:
                            TLog.success("    (value={})".format(char.read()))
        except:  # noqa: E722
            self.reason = "Exception caught: {}".format(sysexcinfo())
        finally:
            device.disconnect()
        if self.found is False and self.reason is None:
            self.reason = "Couldn't find any devices"
