"""Wrapper for the MQTT features."""
from paho.mqtt import publish, subscribe
from paho.mqtt.client import Client, MQTTv31, MQTTv311, connack_string


class SimpleMqttClient:
    """
    A wrapper around simple publish and subscribe methods in paho mqtt. It
    also few implements helper methods.
    """

    @staticmethod
    def sub(topics, **kwargs):
        """
        Wrapper around paho-mqtt subscribe.simple() method. For details on
        arguments. Please refer paho/mqtt/subscribe.py in paho-mqtt project
        (https://pypi.org/project/paho-mqtt/).

        :param topics: Either a string containing a single topic or a list
                       containing multiple topics
        :param kwargs: subscribe.simple() keyword arguments
        :return: List of msg_count messages (from the topics subscribed to)
                 received from the broker.
                 msg_count subscribe.simple() argument is the count of
                 messages to retrieve.
        """
        msgs = subscribe.simple(topics, **kwargs)
        if msgs.__class__ is not list:
            msgs = [msgs]
        return msgs

    @staticmethod
    def pub(topic, **kwargs):
        """
        Wrapper around paho-mqtt publish.single() method. For details on
        arguments, please refer paho/mqtt/publish.py in paho-mqtt project
        (https://pypi.org/project/paho-mqtt/).

        :param topic: Topic to which the messahed will be published.
        :param kwargs: publish.single() keyword arguments
        :return:
        """
        publish.single(topic, **kwargs)

    @staticmethod
    def pubmultiple(msgs, **kwargs):
        """
        Wrapper around paho-mqtt publish.multiple() method. For details on
        arguments, please refer paho/mqtt/publish.py in paho-mqtt project
        (https://pypi.org/project/paho-mqtt/).

        :param msgs: List of messages to publish. Based on paho-mqtt doc,
                     each message can either be:
          1. dict: msg = {'topic':"<topic>", 'payload':"<payload>", 'qos':<qos>
          2. tuple: ("<topic>", "<payload>", qos, retain)
        :param kwargs: publish.multiple() keyword arguments
        :return:
        """
        publish.multiple(msgs, **kwargs)

    @staticmethod
    def connauth(host, client_id=None, user=None, passwd=None, **kw):
        """
        Helper to check if a client can connect to a broker with specific
        client ID and/or credentials.

        :param host: Host to connect to
        :param client_id: Client ID to use. If not specified paho-mqtt
                        generates a random id.
        :param user: User name of the client. If None or empty, connection is
                     attempted without username and password
        :param passwd: Password of the client. If None, only user name is sent
        :param kw: Client.connect() keyword arguments (excluding host)
        :return: Two comma separated values. The result code and its string
                 representation
        """
        return_code = {"rc": None}
        client = Client(client_id, userdata=return_code)
        if user is not None and user != "":
            client.username_pw_set(user, passwd)
        client.on_connect = SimpleMqttClient._on_connauth

        client.connect(host, **kw)
        client.loop_forever()
        return return_code["rc"], connack_string(return_code["rc"])

    @staticmethod
    def _on_connauth(client, userdata, flags, return_code):
        """
        Callback method for paho-mqtt Client. The arguments are passed by
        Client object. Details of the arguments are documented in
        paho/mqtt/client.py (https://pypi.org/project/paho-mqtt/.

        This method is internally used for connauth().

        :param client: The client instance for this callback
        :param userdata: The private user data as set in Client() or
                         userdata_set()
        :param flags: Response flags sent by the broker
        :param return_code: The connection result
        :return: None
        """
        userdata["rc"] = return_code
        client.disconnect()


class MqttClient(Client):
    """Representation of a MQTT client class."""

    pass
