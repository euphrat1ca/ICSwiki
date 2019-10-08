"""Test for getting data from a CoAP device."""

from expliot.core.tests.test import Test, TCategory, TTarget

# from expliot.core.protocols.internet.coap import SimpleCoapClient


class CoapGet(Test):
    """Test for getting data from a CoAP device."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="get",
            summary="CoAP GET",
            descr="This test allows you to send a CoAP GET request (Message) "
            "to a CoAP server on a specified resource path.",
            author="Aseem Jakhar",
            email="aseemjakhar@gmail.com",
            ref=["https://tools.ietf.org/html/rfc7252"],
            category=TCategory(TCategory.COAP, TCategory.SW, TCategory.RECON),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-r",
            "--rhost",
            required=True,
            help="Hostname/IP address of the target CoAP Server",
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=5683,
            type=int,
            help="Port number of the target CoAP Server. Default is 5683",
        )
        self.argparser.add_argument(
            "-u",
            "--path",
            default="/.well-known/core",
            help="Resource URI path of the GET request. Default is discover URI path /.well-known/core",
        )

    def execute(self):
        """Execute the test."""
        # TLog.generic("Sending GET request for URI Path ({}) to CoAP Server {} on port {}".format(self.args.path,
        #                                                                                         self.args.rhost,
        #                                                                                         self.args.rport))
        # clnt = SimpleCoapClient(self.args.rhost, self.args.rport)
        # resp = clnt.get(self.args.path)

        # TLog("resp class {} resp pretty_print {}".format(resp.__class__.__name__, resp.pretty_print()))

        self.result.setstatus(passed=False, reason="CoAP not implemented yet")
