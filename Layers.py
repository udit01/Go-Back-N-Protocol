from Host import *
from Node import *
import time
import threading



class Packet():
	def __init__(self, info="", num=0):
		self.info = info
		self.type = num
		# 0 stands for normal no error packet
		# 1 stands for Termination packet
		#  Different codes for different type of error packets

	

class Frame():
	def __init__(self, info = "", seq = 0, ack = 0, num = 0):
		# super().__init__(info = info)
		# Payload
		self.info = info
		# Sequence number in window
		self.seq = seq
		# Number of packet to send next
		self.ack = ack
		self.type = num
	
	def serialize(self):
		st = str(self.seq)
		st += ";"
		st += self.info
		st += ";"
		st += str(self.ack)
		st += ";"
		st += str(self.type)
		st += ";"
		# st.encode()
		return st.encode()

	def deserialize(self, b):
		str = b.decode()
		l = str.split(';')
		if (l[0] == ''):
			self.seq = -1
		else:
			self.seq = int(l[0])
		self.info = l[1]
		self.ack = int(l[2])
		self.type = int(l[3])
		if (len(l) == 6 ):
			self.type = int(l[4])


class NetworkLayer():
	def __init__(self, infilepath='./data/test.txt', outfilepath='./data/recv.txt'):
		self.packetsToSend = []
		self.packetsReceived = []
		self.infilepath = infilepath
		self.outfilepath = outfilepath
		self.event = 0
		self.make_packets(self.infilepath)

		
	def enable(self):
		pass
	def disable(self):
		pass
	
	# returns a packet to send
	def get_packet(self):

		# if sending packets fin then send an end packet
		# ELSE SEND NORMAL PACKETS 
		if(self.nextPacketToSend >= self.dataSize) :
			self.event = -1
			return Packet( "", 1)
			# Send a packet with "END" STRING OR A PACKET OF DIFFERENT TYPE
		p = self.packetsToSend[self.nextPacketToSend]
		self.nextPacketToSend += 1

		return p

	def write_to_file(self, filepath = "b.txt"):
		
		strings = [packet.info for packet in self.packetsReceived]
		data = " ".join(strings)

		with open(filepath, 'w') as outfile:
			outfile.write(data)
		
		

	# def to_network_layer(self, info):
	def to_network_layer(self, data, type):

		print("IN network layer , got packet of type : ", type)
				
		# if last packet then , call the write file function 
		if type == 1 : 
			self.write_to_file()
			return 1 
			# This code means that the last packet has been received and we need to close the connection now
		
		self.packetsReceived.append(Packet(data))
		return 0

	def make_packets(self, filepath):
		with open(filepath, 'r') as infile:
			lines = infile.readlines()
			
		self.packetsToSend = [Packet(line, 0) for line in lines]
		
		self.dataSize = len(self.packetsToSend)
		self.nextPacketToSend = 0


class PhysicalLayer():
	def __init__(self, ip, port):

		self.buf = []
		s = socket.socket()
		self.max_wait = 10
		self.event = 10
		
		try : 
			s.bind((ip, port))
			s.listen(1)
			self.sock, addr = s.accept()
			print("Server made on", ip, port)
		except Exception:
			s.connect((ip, port))
			self.sock = s
			print("Client made on", ip, port)
		
		# self.sendingThread = threading.Thread(target=self.send, args=("Physical Layer's Sending thread"))
		self.recThread = threading.Thread(target=self.receive, args=("Physical Layer's Receiving thread",))

	def close(self):
		pass


	# def wait_for_event():

	#     self.start()
	#     if self.event == 1 :
	#         self.event = 5 # NO pacekt
	#         return  1
	#     else :
	#         return 5

	def start(self):
		# self.sendingThread.start()
		self.recThread.start()

	def send(self, frame):
		
		print ("Sending: " + str(frame))
		self.sock.send(frame.serialize())

	def receive(self, name):
		time_initial = time.time()
		time_final = time.time()
		time_elapsed = time_final - time_initial
		
		while (True): #time_elapsed < self.max_wait
			print("in receiver", self.event)
			data = self.sock.recv(10)     #Buffer we want to receive is max of 1024 bytes 
			if (not data and self.event == 10) :
				self.event = 5
				break
			else : 
				
				f = Frame()
				print ("Data receieved in Physical layer's receive function : ", data)
				f.deserialize(data)
				self.buf.append(f)
				print("Info of deserialized data : ", f.info)
				print("Type of deserialized data : ", f.type)
				print("Size of Buf: ", len(self.buf))
				time_initial = time.time() 
				#Starting timer again after getting data
				self.event = 1

			time_final = time.time()
			time_elapsed = time_final - time_initial
		self.event = 3
		#Close the thread since timed out

	def enable(self,):
		pass
	def disable(self):
		pass
	def get_packet(self,):
		pass
	def wait_for_event(self,):
		# return 0 or 2(etc) when sending or receiving 
		pass
	def to_physical_layer(self, ):
		pass