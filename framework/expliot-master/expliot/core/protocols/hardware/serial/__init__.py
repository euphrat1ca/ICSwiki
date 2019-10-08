"""Wrapper for the serial interface."""
# pylint: disable=too-many-ancestors
from serial import Serial as Pserial


class Serial(Pserial):
    """A wrapper around pyserial's Serial class."""

    def readfull(self, bsize=1):
        """
        Read from the serial device, bsize at a time and return the complete
        response.
        Please note if timeout is not set for the Serial object, then this
        method will block (on read).

        :param bsize: Size of buffer to pass to read() method
        :return: bytes containing the complete response from the serial device
        """
        read_data = b""
        while True:
            reading = self.read(bsize)
            if not reading:
                break
            read_data += reading
        self.flush()
        return read_data
