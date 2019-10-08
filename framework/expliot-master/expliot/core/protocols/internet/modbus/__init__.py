"""Wrapper for the Modbus integration."""
from pymodbus.client.sync import ModbusTcpClient as MBTClient


class ModbusTcpClient(MBTClient):
    """Wrapper for the Modbus client."""
    pass
