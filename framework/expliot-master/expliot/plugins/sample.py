"""Sample test/plugin as demo."""
from expliot.core.tests.test import Test, TCategory, TTarget, TLog


class Sample(Test):
    """Test class for the sample."""

    def __init__(self):
        """Initialize the test."""
        super().__init__(
            name="Sample",
            summary="Sample Summary",
            descr="Sample Description",
            author="Sample author",
            email="email@example.com",
            ref=["https://example.com", "https://example.dom"],
            category=TCategory(TCategory.COAP, TCategory.SW, TCategory.EXPLOIT),
            target=TTarget(TTarget.GENERIC, TTarget.GENERIC, TTarget.GENERIC),
        )

        self.argparser.add_argument(
            "-r", "--rhost", required=True, help="IP address of the target"
        )
        self.argparser.add_argument(
            "-p",
            "--rport",
            default=80,
            type=int,
            help="Port number of the target. Default is 80",
        )
        self.argparser.add_argument(
            "-v", "--verbose", action="store_true", help="show verbose output"
        )

    def pre(self):
        """Run before the test."""
        TLog.generic("Enter {}.pre()".format(self.id))
        # Only implement this if you need to do some setup etc.
        TLog.generic("Exit {}.pre()".format(self.id))

    def post(self):
        """Run after the test."""
        TLog.generic("Enter {}.post()".format(self.id))
        # Only implement this if you need to do some cleanup etc.
        TLog.generic("Exit {}.post()".format(self.id))

    def execute(self):
        """Execute the test."""
        TLog.generic(
            "Sending request to server({}) on port({})".format(
                self.args.rhost, self.args.rport
            )
        )
        TLog.trydo("Searching imaginary database")
        TLog.success("Found matching entry in database - ({})".format("FooEntry"))
        snd = "GET / HTTP/1.1"
        TLog.generic(
            "Sending command to server ({}) on port ({})".format(
                self.args.rhost, self.args.rport
            )
        )
        if self.args.verbose is True:
            TLog.generic("More verbose output. Sending payload ({})".format(snd))
        TLog.fail("No response received")
        TLog.generic("Re-sending command")
        response = "Response received from the server"
        # In case of failure (Nothing to do in case of success)
        if response:
            self.result.setstatus(passed=True, reason="Server is vulnerable")
        else:
            self.result.setstatus(passed=False, reason="Server is not vulnerable")
        # Or in case you want the test to fail with whatever exception occurred as the reason
        # self.result.exception()
