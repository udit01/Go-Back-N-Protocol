from Host import *
from Node import *


class Packet():
	def __init__(self, info=""):
        self.__init__(info, 0)
    def __init__(self, info="", num=0):
        self.info = info
        self.type = num
        # 0 stands for normal no error packet
        # 1 stands for Termination packet
        #  Different codes for different type of error packets 
    

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
    def __init__(self, infilepath='./data/test.txt', outfilepath='./data/recv.txt'):
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
        if(self.nextPacketToSend >= self.dataSize) :
            return Packet( "", 1)
            # Send a packet with "END" STRING OR A PACKET OF DIFFERENT TYPE
        p = self.packetsToSend[self.nextPacketToSend]
        self.nextPacketToSend += 1

        return p

    def write_to_file(self, filepath = self.outfilepath):
        
        strings = [packet.info for packet in self.packetsReceived]
        data = " ".join(strings)

        with open(filepath, 'w') as outfile:
            outfile.write(data)
        
        

    # def to_network_layer(self, info):
    def to_network_layer(self, packet):
        
        # if last packet then , call the write file function 
        if packet.info == 1 : 
            self.write_to_file()
            return 1 
            # This code means that the last packet has been received and we need to close the connection now
        
        self.packetsReceived.append(Packet(info))
        return 0

    def make_packets(filepath):
        with open(filepath, 'r') as infile:
            lines = infile.readlines()
            
        self.packetsToSend = [Packet(line, 0) for line in lines]
        
        self.dataSize = len(self.packetsToSend)
        self.nextPacketToSend = 0


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