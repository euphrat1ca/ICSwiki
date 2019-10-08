"""Support for fuzzing command over a serial connection."""
import itertools

from expliot.core.common.exceptions import sysexcinfo
from expliot.core.protocols.hardware.serial import Serial
from expliot.core.tests.test import TCategory, Test, TLog, TTarget


# pylint: disable=too-many-nested-blocks, bare-except
class FuzzCommands(Test):
    """Test to fuzz commands."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="fuzzcmds",
            summary="Serial console command brute-forcer/fuzzer",
            descr="This test helps in finding/fuzzing hidden commands/parameters/back doors in custom consoles, of devices exposed over the UART port on the board. It  sends random words as specified over the serial connection and matches the response to a specified string (case insensitive). Based on match or nomatch criteria it decides whether the word is a valid or invalid command.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=[
                "https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter"
            ],
            category=TCategory(TCategory.UART, TCategory.HW, TCategory.FUZZ),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-b",
            "--baud",
            type=int,
            default=115200,
            help="The Baud rate of the serial device. Default is 115200",
        )
        self.argparser.add_argument(
            "-p",
            "--port",
            default="/dev/ttyUSB0",
            required=True,
            help="The device port on the system. Default is /dev/ttyUSB0",
        )
        self.argparser.add_argument(
            "-c",
            "--chars",
            default="abcdefghijklmnopqrstuvwxyz",
            help="The characters to use for generating random words. Default is abcdefghijklmnopqrstuvwxyz",
        )
        self.argparser.add_argument(
            "-l",
            "--length",
            type=int,
            default=3,
            help="Specify the character length for each generated word. Default is 3 characters",
        )
        self.argparser.add_argument(
            "-x", "--prefix", default="", help="Prefix a string to the generated word"
        )
        self.argparser.add_argument(
            "-a",
            "--append",
            default="\r\n",
            help='Append a string to the generated word. Default is "\\r\\n"',
        )
        self.argparser.add_argument(
            "-m",
            "--match",
            help="Specify a match criteria string. If the response contains this thring, then the word is a valid command. Assumption is based on different responses for valid and invalid commands. Must not be used along with --nomatch",
        )
        self.argparser.add_argument(
            "-n",
            "--nomatch",
            help="Specify a nomatch criteria string. If the response doesn't contain this string, then the word is a valid command. Assumption is based on different responses for valid and invalid commands. Must not used along with --match",
        )
        self.argparser.add_argument(
            "-s",
            "--stop",
            action="store_true",
            help="Stop after finding one valid command",
        )
        self.argparser.add_argument(
            "-t",
            "--timeout",
            type=float,
            default=0.5,
            help="Read timeout, in secs, for the serial device. Default is 0.5",
        )
        self.argparser.add_argument(
            "-z",
            "--buffsize",
            type=int,
            default=1,
            help="Read buffer size. change this and timeout to increase efficiency. Default is 1",
        )
        self.argparser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Show verbose output i.e. each word",
        )

    def pre(self):
        """Pre task for the test."""
        if self.args.match is None:
            if self.args.nomatch is None:
                raise AttributeError("Specify either --match or --nomatch")
        elif self.args.nomatch is not None:
            raise AttributeError("Can't specify both --match and --nomatch")

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Connecting to the the serial port ({}) with baud ({})".format(
                self.args.port, self.args.baud
            )
        )
        TLog.generic(
            "Using chars({}) and length({})".format(self.args.chars, self.args.length)
        )
        found = False
        reason = "Couldn't find a valid command"
        commands = []
        tries = 0
        sock = None
        try:
            sock = Serial(self.args.port, self.args.baud, timeout=self.args.timeout)
            for word in itertools.product(self.args.chars, repeat=self.args.length):
                cmd = self.args.prefix + "".join(word) + self.args.append
                sock.write(cmd.encode())
                received_data = sock.readfull(self.args.buffsize)
                sock.flush()
                tries += 1
                if tries % 20 == 0:
                    # Print something to engage the user :)
                    TLog.generic("Tried {} commands till now".format(tries))
                if self.args.verbose is True:
                    TLog.trydo(
                        "Command=({}) response({})".format(cmd.rstrip(), received_data)
                    )
                if self.args.match is not None:
                    if self.args.match.lower() in received_data.decode().lower():
                        TLog.success(
                            "Command=({}) found. --match criteria in Response=({})".format(
                                cmd.rstrip(), received_data
                            )
                        )
                        found = True
                        commands.append(cmd.rstrip())
                        if self.args.stop is True:
                            break
                elif self.args.nomatch is not None:
                    if self.args.nomatch.lower() not in received_data.decode().lower():
                        TLog.success(
                            "Command=({}) found. --nomatch criteria in response=({})".format(
                                cmd.rstrip(), received_data
                            )
                        )
                        found = True
                        commands.append(cmd.rstrip())
                        if self.args.stop is True:
                            break
        except:  # noqa: E722
            reason = "Exception caught: {}".format(sysexcinfo())
        finally:
            if sock:
                sock.close()
        if found is True:
            TLog.success("Valid commands found: ({})".format(commands))
        else:
            self.result.setstatus(passed=False, reason=reason)
