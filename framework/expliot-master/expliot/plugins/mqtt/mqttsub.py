"""Plugin to subscribe to a topic of a MQTT broker."""
from expliot.core.protocols.internet.mqtt import SimpleMqttClient
from expliot.core.tests.test import Test, TCategory, TTarget, TLog
from expliot.plugins.mqtt import DEFAULT_MQTT_PORT, MQTT_REFERENCE


# pylint: disable=bare-except
class MqttSub(Test):
    """Subscribe to a topic of a MQTT broker."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="sub",
            summary="MQTT Subscriber",
            descr="This test allows you to subscribe to a topic on an MQTT "
            "broker and read messages being published on that topic.",
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
            default="$SYS/#",
            help="Topic filter to subscribe on the MQTT broker. Default is " "$SYS/#",
        )
        self.argparser.add_argument(
            "-c",
            "--count",
            default=1,
            type=int,
            help="Specify count of messages to read. It blocks till all the"
            "(count)  messages are read. Default is 1",
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
            "Subscribing to topic ({}) on MQTT broker ({}) on port ({})".format(
                self.args.topic, self.args.rhost, self.args.rport
            )
        )
        try:
            credentials = None
            if self.args.user and self.args.passwd:
                credentials = {"username": self.args.user, "password": self.args.passwd}
                TLog.trydo(
                    "Using authentication (username={})(password={})".format(
                        self.args.user, self.args.passwd
                    )
                )

            messages = SimpleMqttClient.sub(
                self.args.topic,
                hostname=self.args.rhost,
                port=self.args.rport,
                client_id=self.args.id,
                auth=credentials,
                msg_count=self.args.count,
            )
            for message in messages:
                TLog.success(
                    "(topic={})(payload={})".format(message.topic, str(message.payload))
                )
        except:  # noqa: E722
            self.result.exception()
