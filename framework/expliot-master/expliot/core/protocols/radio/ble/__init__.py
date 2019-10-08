"""Support for BLE."""
from bluepy import btle


class Ble:
    """A wrapper around simple BLE operations."""

    ADDR_TYPE_RANDOM = btle.ADDR_TYPE_RANDOM
    ADDR_TYPE_PUBLIC = btle.ADDR_TYPE_PUBLIC
    # Advertising Data Type value for "Complete Local Name"
    # Ref: https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile
    ADTYPE_NAME = 9

    @staticmethod
    def scan(iface=0, tout=10):
        """Scan for BLE devices."""
        scanner = BleScanner(iface)
        scanentries = scanner.scan(timeout=tout)
        return scanentries


class BleScanner(btle.Scanner):
    """A wrapper around bluepy Scanner class."""

    pass


class BlePeripheral(btle.Peripheral):
    """A wrapper around bluepy Peripheral class."""

    pass
