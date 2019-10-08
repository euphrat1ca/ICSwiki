"""Wrapper for CANbus communication."""
from can.interface import Bus
from can import Message


class CanBus(Bus):
    """A simple wrapper around python-can Bus class."""

    pass


class CanMessage(Message):
    """A simple wrapper around python-can Message class."""

    pass
