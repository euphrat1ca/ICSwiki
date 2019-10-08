"""Support for reading data from Modbus over TCP."""
from expliot.core.protocols.internet.modbus import ModbusTcpClient
from expliot.core.tests.test import TCategory, Test, TLog, TTarget
from expliot.plugins.modbus import (
    COIL,
    DINPUT,
    HREG,
    IREG,
    MODBUS_REFERENCE,
    READ_ITEMS,
)


# pylint: disable=bare-except
class MBTcpRead(Test):
    """Test for reading data from Modbus over TCP."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="readtcp",
            summary="Modbus TCP Reader",
            descr="This plugin reads the item (coil, discrete input, holding "
            "and input register)values from a Modbus server.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=MODBUS_REFERENCE,
            category=TCategory(TCategory.MODBUS, TCategory.SW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-r",
            "--rhost",
            required=True,
            help="The hostname/IP address of the Modbus server",
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=502,
            type=int,
            help="The port number of the Modbus server. Default is 502",
        )
        self.argparser.add_argument(
            "-i",
            "--item",
            default=0,
            type=int,
            help="The item to read from. {coil} = {}, {} = {}, {} = {}, {} = {}. Default is {coil}".format(
                READ_ITEMS[COIL],
                DINPUT,
                READ_ITEMS[DINPUT],
                HREG,
                READ_ITEMS[HREG],
                IREG,
                READ_ITEMS[IREG],
                coil=COIL,
            ),
        )
        self.argparser.add_argument(
            "-a",
            "--address",
            default=0,
            type=int,
            help="The start address of item to read from",
        )
        self.argparser.add_argument(
            "-c",
            "--count",
            default=1,
            type=int,
            help="The count of items to read. Default is 1",
        )
        self.argparser.add_argument(
            "-u",
            "--unit",
            default=1,
            type=int,
            help="The Unit ID of the slave on the server to read from.",
        )

    def execute(self):
        """Execute the test."""
        modbus_client = ModbusTcpClient(self.args.rhost, port=self.args.rport)

        try:
            if self.args.item < 0 or self.args.item >= len(READ_ITEMS):
                raise AttributeError(
                    "Unknown --item specified ({})".format(self.args.item)
                )

            TLog.generic(
                "Sending read command to Modbus Server ({}) on port ({})".format(
                    self.args.rhost, self.args.rport
                )
            )
            TLog.generic(
                "(item={})(address={})(count={})(unit={})".format(
                    READ_ITEMS[self.args.item],
                    self.args.address,
                    self.args.count,
                    self.args.unit,
                )
            )
            modbus_client.connect()
            if self.args.item == self.COIL:
                response = modbus_client.read_coils(
                    self.args.address, self.args.count, unit=self.args.unit
                )
                if response.isError() is True:
                    raise Exception(str(response))
                values = response.bits
            elif self.args.item == self.DINPUT:
                response = modbus_client.read_discrete_inputs(
                    self.args.address, self.args.count, unit=self.args.unit
                )
                if response.isError() is True:
                    raise Exception(str(response))
                values = response.bits
            elif self.args.item == self.HREG:
                response = modbus_client.read_holding_registers(
                    self.args.address, self.args.count, unit=self.args.unit
                )
                if response.isError() is True:
                    raise Exception(str(response))
                values = response.registers
            elif self.args.item == self.IREG:
                response = modbus_client.read_input_registers(
                    self.args.address, self.args.count, unit=self.args.unit
                )
                if response.isError() is True:
                    raise Exception(str(response))
                values = response.registers
            else:
                raise AttributeError(
                    "Unknown --item specified ({})".format(self.args.item)
                )
            for entry in range(0, self.args.count):
                TLog.success(
                    "({}[{}]={})".format(
                        READ_ITEMS[self.args.item],
                        self.args.address + entry,
                        values[entry],
                    )
                )
        except:  # noqa: E722
            self.result.exception()
        finally:
            modbus_client.close()
