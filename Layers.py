from Host import *
from Node import *


class Packet():
	def __init__(self, info=""):
        self.info = info

class Frame(Packet):
	def __init__(self, info = "", seq = 0, ack = 0):
		
        self.__init__(super, info = info)
		# Payload
		# self.info = info
		# Sequence number in window
		self.seq = seq
		# Number of packet to send next
		self.ack = ack



class NetworkLayer():
    def __init__(self, infilepath='./data/test.txt', outfilepath='./data/recv.txt', ):
        self.packetsToSend = []
        self.packetsReceived = []
        self.infilepath = infilepath
        self.outfilepath = outfilepath
        self.make_packet(self.infilepath)
        
    def enable(self):
        pass
    def disable(self):
        pass
    def get_packet(self):

        # if sending packets fin then send an end packet 
        # ELSE SEND NORMAL PACKETS 
        pass
    
    def write_to_file(self, filepath = self.outfilepath):
        
        with open(filepath, 'w') as outfile:
            for packet in self.packetsReceived:
                outfile.write(packet.info)
        
        

    def to_network_layer(self, info):
        
        # if last packet then , call the write file function 

        self.packetsReceived.append(Packet(info))
        
    def make_packets(filepath):
        with open(filepath, 'r') as infile:
            lines = infile.readlines()
            
        self.packetsToSend = [Packet(line) for line in lines]
        


class PhysicalLayer():
    def __init__(self, ):
        pass
    def enable(self,):
        pass
    def disable(self):
        pass
    def get_packet(self,):
        pass
    def wait_for_event(self,):
        pass
    def to_physical_layer(self, ):
        pass