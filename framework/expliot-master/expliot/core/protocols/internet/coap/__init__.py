"""Wrapper for the CoAP communication."""

# from coapthon.client.helperclient import HelperClient
# import logging
# from pathlib import Path
# import os
# my_file = Path("logging.conf")
# if my_file.is_file():
#     print("logging.conf exists")
#
# else:
#     print("logging.conf DOESN'T exist")
#
# # CoAPthon3 (1.0.1) version creates file logging.conf and sets log level to debug
# # They have fixed the issue but the Python package is not yet released. Until then
# # lets disable logging and delete file ourselves
# #
# logging.disable(logging.CRITICAL)
#
# class SimpleCoapClient(HelperClient):
#     """
#     A wrapper around HelperClient in coapthon
#     """
#     def __init__(self, host, port):
#         super().__init__(server=(host,port))
