"""Test the authentication of a MQTT broker."""
from expliot.core.common.fileutils import readlines
from expliot.core.protocols.internet.mqtt import SimpleMqttClient
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.plugins.mqtt import DEFAULT_MQTT_PORT, MQTT_REFERENCE


# pylint: disable=bare-except
class MqttAuth(Test):
    """Test the authentication of a MQTT broker."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="crackauth",
            summary="MQTT authentication cracker",
            descr="This test case attempts to crack the MQTT authentication"
            "with the specified credentials. You need specify the user "
            "and password or password dictionary.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=[MQTT_REFERENCE],
            category=TCategory(TCategory.MQTT, TCategory.SW, TCategory.ANALYSIS),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-r",
            "--rhost",
            required=True,
            help="Hostname/IP address of the target MQTT broker",
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=DEFAULT_MQTT_PORT,
            type=int,
            help="Port number of the target MQTT broker. Default is 1883",
        )
        self.argparser.add_argument(
            "-i",
            "--id",
            help="The client ID to be used for the connection. Default is"
            "random client ID",
        )
        self.argparser.add_argument(
            "-u", "--user", help="Specify the user name to be used"
        )
        self.argparser.add_argument(
            "-w", "--passwd", help="Specify the password to be used"
        )
        self.argparser.add_argument(
            "-f",
            "--pfile",
            help="Specify the file containing passwords, one per line. If"
            "this option is present, --pass option will be ignored",
        )
        self.argparser.add_argument(
            "-v", "--verbose", action="store_true", help="Show verbose output)"
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Attempting to authenticate with the MQTT broker ({}) on port "
            "({})".format(self.args.rhost, self.args.rport)
        )
        found = False
        try:
            if self.args.pfile and self.args.user:
                for password in readlines(self.args.pfile):
                    if self.args.verbose:
                        TLog.generic(
                            "Checking username {} with password {}".format(
                                self.args.user, password
                            )
                        )
                    return_code, state = SimpleMqttClient.connauth(
                        self.args.rhost,
                        client_id=self.args.id,
                        user=self.args.user,
                        passwd=password,
                        port=self.args.rport,
                    )
                    if return_code == 0:
                        TLog.success(
                            "FOUND - (user={})(passwd={})(return code={}:{})".format(
                                self.args.user, password, return_code, state
                            )
                        )
                        found = True
                        break
                    elif self.args.verbose:
                        TLog.fail(
                            "Auth failed - (user={})(passwd={})(return code={}:{})".format(
                                self.args.user, password, return_code, state
                            )
                        )
                if found is False:
                    self.result.setstatus(
                        passed=False, reason="Auth failed for all passwords"
                    )
            else:
                return_code, state = SimpleMqttClient.connauth(
                    self.args.rhost,
                    client_id=self.args.id,
                    user=self.args.user,
                    passwd=self.args.passwd,
                    port=self.args.rport,
                )
                if return_code == 0:
                    TLog.success(
                        "FOUND - (user={})(passwd={})(return code={}:{})".format(
                            self.args.user, self.args.passwd, return_code, state
                        )
                    )
                else:
                    self.result.setstatus(passed=False, reason=state)
                    if self.args.verbose:
                        TLog.fail(
                            "Auth failed - (user={})(passwd={})(return code={}:{})".format(
                                self.args.user, self.args.passwd, return_code, state
                            )
                        )
        except:  # noqa: E722
            self.result.exception()
