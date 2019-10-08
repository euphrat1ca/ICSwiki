"""Support for writing data over i2c."""
from time import time

from expliot.core.protocols.hardware.i2c import I2cEepromManager
from expliot.core.tests.test import TCategory, Test, TLog, TTarget


# pylint: disable=bare-except
class I2cEepromWrite(Test):
    """Write test for data to i2c."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="writeeeprom",
            summary="I2C EEPROM Writer",
            descr="This plugin writes data to an I2C EEPROM chip. It needs an "
            "FTDI interface to write data to the target EEPROM chip. You "
            "can buy an FTDI device online. If you are interested we have "
            "an FTDI based product - 'Expliot Nano' which you can order online "
            "from www.expliot.io This plugin uses pyi2cflash package which in "
            "turn uses pyftdi python driver for ftdi chips. For more details "
            "on supported I2C EEPROM chips, check the readme at https://github.com/eblot/pyi2cflash "
            "Thank you Emmanuel Blot for pyi2cflash. You may want to run it as "
            "root in case you  get a USB error related to langid.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=["https://github.com/eblot/pyspiflash"],
            category=TCategory(TCategory.I2C, TCategory.HW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-a",
            "--addr",
            default=0,
            type=int,
            help="Specify the start address where data is to be written. Default is 0",
        )
        self.argparser.add_argument(
            "-u",
            "--url",
            default="ftdi:///1",
            help="URL of the connected FTDI device. Default is ftdi:///1. For "
            "more details on the URL scheme check https://eblot.github.io/pyftdi/urlscheme.html",
        )
        self.argparser.add_argument(
            "-c",
            "--chip",
            required=True,
            help="Specify the chip. Supported chips are 24AA32A, 24AA64, 24AA128, 24AA256, 24AA512",
        )
        self.argparser.add_argument(
            "-d",
            "--data",
            help="Specify the data to write, as hex stream, without the 0x prefix",
        )
        self.argparser.add_argument(
            "-r",
            "--rfile",
            help="Specify the file path from where data is to be read. This takes "
            "precedence over --data option i.e if both options are specified --data would be ignored",
        )
        self.slaveaddr = 0x50

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Writing data to i2c eeprom at address({}) using device({})".format(
                self.args.addr, self.args.url
            )
        )
        try:
            start_address = self.args.addr
            if self.args.rfile:
                TLog.trydo("Reading data from the file ({})".format(self.args.rfile))
                input_file = open(self.args.rfile, "r+b")
                data = input_file.read()
                input_file.close()
            elif self.args.data:
                data = bytes.fromhex(self.args.data)
            else:
                raise AttributeError("Specify either --data or --rfile (but not both)")

            device = I2cEepromManager.get_flash_device(
                self.args.url, self.args.chip, address=self.slaveaddr
            )
            TLog.success("(chip size={} bytes)".format(len(device)))

            length_data = len(data)
            TLog.trydo(
                "Writing {} byte(s) at start address {}".format(
                    length_data, start_address
                )
            )
            if self.args.addr + length_data > len(device):
                raise IndexError("Length is out of range of the chip size")
            start_time = time()
            device.write(start_address, data)
            end_time = time()
            TLog.success(
                "wrote {} byte(s) of data from address {}. Time taken {} secs".format(
                    len(data), start_address, round(end_time - start_time, 2)
                )
            )
        except:  # noqa: E722
            self.result.exception()
        finally:
            I2cEepromManager.close(device)
