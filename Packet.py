#!/usr/bin/python

class DataFrame():
    """
    Packet class for go back n protocol 
    """
    # everything is in bits
    HEADER_SIZE = 256
    MIN_PAYLOAD_SIZE = 512 - HEADER_SIZE 
    MAX_PAYLOAD_SIZE = 2024 - HEADER_SIZE

    pass

class AckFrame():
    """
    Ack class 
    """
    HEADER_SIZE = 256
    PAYLOAD_SIZE = 0
    pass