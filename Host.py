#!/usr/bin/python

import os
import sys
import socket
from threading import Thread

class Host(Thread):
    """
    HOST running Go-Back-N protocol for reliable data transfer.
    Both sender and receiever
    """

    def __init__(self,
                receiverIP="127.0.0.1",
                receiverPort=8080,
                sequenceNumberBits=2,
                www=os.path.join(os.getcwd(), "data", "receiver")):
        self.receiverIP = receiverIP
        self.receiverPort = receiverPort
        self.sequenceNumberBits = sequenceNumberBits
        self.www = www
        # WWW is the data path