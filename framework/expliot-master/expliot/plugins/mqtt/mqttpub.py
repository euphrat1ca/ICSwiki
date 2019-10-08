"""Plugin to publish to a topic of a MQTT broker."""
from expliot.core.protocols.internet.mqtt import SimpleMqttClient
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.plugins.mqtt import DEFAULT_MQTT_PORT, MQTT_REFERENCE


# pylint: disable=bare-except
class MqttPub(Test):
    """Publish a MQTT message to a given MQTT broker."""

    def __init__(self):
        """Initialize the test."""

        super().__init__(
            name="pub",
            summary="MQTT Publisher",
            descr="This test case publishes a message on a topic to a"
            "specified MQTT broker on a specified port.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=[MQTT_REFERENCE],
            category=TCategory(TCategory.MQTT, TCategory.SW, TCategory.RECON),
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
            "-t",
            "--topic",
            required=True,
            help="Topic name on which message has to be published",
        )
        self.argparser.add_argument(
            "-m",
            "--msg",
            required=True,
            help="Message to be published on the specified topic",
        )
        self.argparser.add_argument(
            "-i",
            "--id",
            help="The client ID to be used for the connection. Default is "
            "random client ID",
        )
        self.argparser.add_argument(
            "-u",
            "--user",
            help="Specify the user name to be used. If not specified, it "
            "connects without authentication",
        )
        self.argparser.add_argument(
            "-w",
            "--passwd",
            help="Specify the password to be used. If not specified, it "
            "connects with without authentication",
        )

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Publishing message on topic ({}) to MQTT Broker ({}) on port "
            "({})".format(self.args.rhost, self.args.topic, self.args.rport)
        )
        credentials = None
        if self.args.user and self.args.passwd:
            credentials = {"username": self.args.user, "password": self.args.passwd}
            TLog.trydo(
                "Using authentication (username={})(password={})".format(
                    self.args.user, self.args.passwd
                )
            )
        try:
            SimpleMqttClient.pub(
                self.args.topic,
                payload=self.args.msg,
                hostname=self.args.rhost,
                port=self.args.rport,
                auth=credentials,
                client_id=self.args.id,
            )
            TLog.success("Done")
        except:  # noqa: E722
            self.result.exception()
