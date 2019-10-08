"""Main part to start """
import argparse

from expliot.core.ui.cli import Cli
from expliot.core.tests.test import TLog

from expliot.constants import BANNER


class EfCli:
    """The interactive console and CLI interface for EXPLIoT framework."""

    cli = Cli(prompt="ef> ", intro=BANNER)

    @classmethod
    def main(cls):
        """
        Run a single command given on the command line or run the main command
        loop of the console if no command line arguments given.

        :return:
        """
        TLog.init()

        parser = argparse.ArgumentParser(
            description="Expliot - Internet Of Things Security Testing and "
            "Exploitation Framework Command Line Interface."
        )

        parser.add_argument(
            "cmd",
            nargs="?",
            help="Command to execute. If no command is given, it enters an "
            "interactive console. To see the list of available commands "
            "use the help command",
        )
        parser.add_argument(
            "cmd_args",
            nargs=argparse.REMAINDER,
            help="Sub-command and/or (optional) arguments",
        )

        args = parser.parse_args()

        if args.cmd:
            # Execute a single command and exit
            cls.cli.onecmd_plus_hooks("{} {}".format(args.cmd, " ".join(args.cmd_args)))
        else:
            # No command line argument specified, drop into interactive mode
            cls.cli.cmdloop()


if __name__ == "__main__":
    EfCli.main()
