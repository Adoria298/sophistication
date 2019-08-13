"""
Based on https://www.realpython.com/python-sockets .
Used to communicate between classes, internally.
"""
import sys
import selectors
import json
import io
import struct

class _Message:
    pass

class ServerMessage(_Message):
    pass

class ClientMessage(_Message):
    pass
