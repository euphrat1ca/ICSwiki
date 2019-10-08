"""Support for interacting with Modbus over TCP."""
MODBUS_REFERENCE = [
    "https://en.wikipedia.org/wiki/Modbus",
    "http://www.modbus.org/specs.php",
]

COIL = 0
DINPUT = 1
HREG = 2
IREG = 3
READ_ITEMS = ["coil", "discrete input", "holding register", "input register"]
REG = 1
WRITE_ITEMS = ["coil", "register"]
