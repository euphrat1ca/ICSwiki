"""Support for reading data from SPI."""
from time import time

from expliot.core.protocols.hardware.spi import SpiFlashManager
from expliot.core.tests.test import TCategory, Test, TLog, TTarget


# pylint: disable=bare-except
class SPIFlashRead(Test):
    """Test to read data from SPI."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="readflash",
            summary="SPI Flash Reader",
            descr="This plugin reads data from a serial flash chip that implements SPI protocol. It needs a FTDI interface to read data from the target flash chip. You can buy an FTDI device online. If you are interested we have an FTDI based product - 'Expliot Nano' which you can order online from www.expliot.io. This plugin uses pyspiflash package which in turn uses pyftdi python driver for FTDI chips. For more details on supported flash chips, check the readme at https://github.com/eblot/pyspiflash. Thank you Emmanuel Blot for pyspiflash. You may want to run it as root in case you get a USB error related to langid.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=["https://github.com/eblot/pyspiflash"],
            category=TCategory(TCategory.SPI, TCategory.HW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-a",
            "--addr",
            default=0,
            type=int,
            help="Specify the start address from where data is to be read. Default is 0",
        )
        self.argparser.add_argument(
            "-l",
            "--length",
            type=int,
            help="Specify the total length of data, in bytes, to be read from the start address. If not specified, it reads till the end",
        )
        self.argparser.add_argument(
            "-u",
            "--url",
            default="ftdi:///1",
            help="URL of the connected FTDI device. Default is ftdi:///1. For more details on the URL scheme check https://eblot.github.io/pyftdi/urlscheme.html",
        )
        self.argparser.add_argument(
            "-f",
            "--freq",
            type=int,
            help="Specify a frequency in Hz(example: 1000000 for 1 MHz. If not, specified, default frequency of the device is used. You may want to decrease the frequency if you keep seeing FtdiError:UsbError.",
        )
        self.argparser.add_argument(
            "-w",
            "--wfile",
            help="Specify the file path where data, read from the SPI flash device, is to be written. If not specified output the data on the terminal.",
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Reading data from SPI flash at address({}) using device ({})".format(
                self.args.addr, self.args.url
            )
        )
        device = None
        try:
            device = SpiFlashManager.get_flash_device(
                self.args.url, freq=self.args.freq
            )
            length = self.args.length or (len(device) - self.args.addr)
            TLog.success(
                "(chip found={})(chip size={} bytes)(using frequency={})".format(
                    device, len(device), int(device.spi_frequency)
                )
            )
            TLog.trydo(
                "Reading {} bytes from start address {}".format(length, self.args.addr)
            )
            if self.args.addr + length > len(device):
                raise IndexError("Length is out of range of the chip size")
            start_time = time()
            data = device.read(self.args.addr, length)
            end_time = time()
            if self.args.wfile:
                TLog.trydo("Writing data to the file ({})".format(self.args.wfile))
                local_file = open(self.args.wfile, "w+b")
                data.tofile(local_file)
                local_file.close()
            else:
                TLog.success("(data={})".format([hex(x) for x in data]))
            TLog.success(
                "Done. Total bytes read ({}) Time taken to read = {} s".format(
                    len(data), round(end_time - start_time, 2)
                )
            )
        except:  # noqa: E722
            self.result.exception()
        finally:
            SpiFlashManager.close(device)
