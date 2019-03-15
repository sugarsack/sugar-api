# coding: utf-8

from fastapi import FastAPI
from sugar.utils.objects import Singleton


apirouter = FastAPI(title="Sugar API", version="0.0.0 Alpha")


@Singleton
class MasterRef:
    """
    Master reference object.
    """
    def __init__(self, channel=None):
        self.receiver, self.sender = channel if channel else (None, None)

    def get(self, property):
        """
        Get an attribute.

        :param property:
        :return:
        """
        self.sender.send(property)
        return self.sender.recv()
