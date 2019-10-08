"""Support for writing data to Modbus over TCP."""
from expliot.core.protocols.internet.modbus import ModbusTcpClient
from expliot.core.tests.test import TCategory, Test, TLog, TTarget
from expliot.plugins.modbus import COIL, MODBUS_REFERENCE, REG, WRITE_ITEMS


# pylint: disable=bare-except
class MBTcpWrite(Test):
    """Test for writing data to Modbus over TCP."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="writetcp",
            summary="Modbus TCP Writer",
            descr="This plugin writes the item (coil, register) values to a "
            "Modbus server.",
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
            help="The item to read from. {coil} = {}, {} = {}. Default is {coil}".format(
                WRITE_ITEMS[COIL], REG, WRITE_ITEMS[REG], coil=COIL
            ),
        )
        self.argparser.add_argument(
            "-a",
            "--address",
            default=0,
            type=int,
            help="The start address of item to write to",
        )
        self.argparser.add_argument(
            "-c",
            "--count",
            default=1,
            type=int,
            help="The count of items to write. Default is 1",
        )
        self.argparser.add_argument(
            "-u",
            "--unit",
            default=1,
            type=int,
            help="The unit ID of the slave on the server to write to",
        )
        self.argparser.add_argument(
            "-w", "--value", required=True, type=int, help="The value to write"
        )

    def execute(self):
        """Execute the test."""
        modbus_client = ModbusTcpClient(self.args.rhost, port=self.args.rport)

        try:
            if self.args.item < 0 or self.args.item >= len(WRITE_ITEMS):
                raise AttributeError(
                    "Unknown --item specified ({})".format(self.args.item)
                )
            if self.args.count < 1:
                raise AttributeError(
                    "Invalid --count specified ({})".format(self.args.count)
                )

            TLog.generic(
                "Sending write command to Modbus Server ({}) on port ({})".format(
                    self.args.rhost, self.args.rport
                )
            )
            TLog.generic(
                "(item={})(address={})(count={})(unit={})".format(
                    WRITE_ITEMS[self.args.item],
                    self.args.address,
                    self.args.count,
                    self.args.unit,
                )
            )
            modbus_client.connect()
            if self.args.item == COIL:
                value = bool(self.args.value != 0)
                TLog.trydo("Writing value(s): {}".format(value))
                response = modbus_client.write_coils(
                    self.args.address, [value] * self.args.count, unit=self.args.unit
                )
                if response.isError() is True:
                    raise Exception(str(response))
            elif self.args.item == REG:
                TLog.trydo("Writing value(s): {}".format(self.args.value))
                response = modbus_client.write_registers(
                    self.args.address,
                    [self.args.value] * self.args.count,
                    unit=self.args.unit,
                )
                if response.isError() is True:
                    raise Exception(str(response))
            else:
                raise AttributeError(
                    "Unknown --item specified ({})".format(self.args.item)
                )
            TLog.success("Values successfully written")
        except:  # noqa: E722
            self.result.exception()
        finally:
            modbus_client.close()
