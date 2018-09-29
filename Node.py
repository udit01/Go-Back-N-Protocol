# /* Protocol 5 (Go-back-n) allows multiple outstanding frames. The sender may transmit up
# to MAX SEQ frames without waiting for an ack. In addition, unlike in the previous
# protocols, the network layer is not assumed to have a new packet all the time. Instead,
# the network layer causes a network layer ready event when there is a packet to send. */

# typedef enum {frame arrival, cksum err, timeout, network layer ready} event type #

from Layers import *


def between(a, b, c):
	# /* Return true if a <= b < c circularly # false otherwise. */
	if (((a <= b) and (b < c)) or ((c < a) and (a <= b)) or ((b < c) and (c < a))):
		return True
	else:
		return False


class seq_nr():
	def __init__(self, num):
		self.val = num
	def inc():
		self.val = self.val + 1
	def dec():
		self.val = self.val - 1


class event_type():
	def __init__(self, inp):
		# 0 -> Frame Arrival
		# 1 -> Checksum Error
		# 2 -> Timeout
		# 3 -> Network Layer Ready
		# 4 -> NULL
		self.type = inp



def wait_for_event():
	e = event_type(4)
	return e

def stop_timer(number):
	pass

class Node():
	def __init__(self, nl, pl ):
		self.networkLayer = nl
		self.physicalLayer = pl
		self.MAX_SEQ = 7


	def start_timer(self, frame_nr):
		pass
	
	def stop_timer(self, ack_no):
		pass

	def send_data(self, next_frame_to_send, frame_expected, buffer):
		# /* Construct and send a data frame. */
		
		packet = buffer[next_frame_to_send]
		
		s = Frame(packet, frame_nr,
				(frame_expected + self.MAX_SEQ) % (self.MAX_SEQ + 1) 
				)
				#/* piggyback ack */
		
		self.physicalLayer.to_physical_layer(s) # /* transmit the frame */
		self.start_timer(frame_nr) #/* start the timer running */


	def protocol5(self) :

		next_frame_to_send = seq_nr(0)# /* MAX SEQ > 1 # used for outbound stream */ # /* next frame going out */
		ack_expected = seq_nr(0)# /* oldest frame as yet unacknowledged */ # /* next ack expected inbound */
		frame_expected = seq_nr(0) # /* next frame expected on inbound stream */ # /* number of frame expected inbound */
		nbuffered = seq_nr(0)  # /* number of output buffers currently in use */ # /* initially no packets are buffered */
		
		r = Frame() # /* scratch variable */

		# packet buffer[self.MAX_SEQ + 1] 
		# /* buffers for the outbound stream */
		buffer = [packet() for i in range(self.MAX_SEQ+1)]
		
		i = seq_nr(0) 
		# /* used to index into the buffer array */
		
		# nl = NetworkLayer()
		self.networkLayer.enable()
		# enable_network_layer()
		# /* allow network layer ready events */


		# Why is this a while truw with break at each seq ?


		while (True):
			
			event = self.physicalLayer.wait_for_event()
			# event = wait_for_event() 
			# /* four possibilities: see event type above */
			
			n = event.type
			
			# Network layer ready
			if n == 0 :
				#  /* the network layer has a packet to send */
				# /* Accept, save, and transmit a new frame. */
				
				# /* fetch new packet */
				buffer[next_frame_to_send.val] = self.networkLayer.get_packet() 
				# packet = get_packet_from_network layer() 
				
				# /* expand the sender’s window */
				nbuffered.inc()
				
				#/* transmit the frame */
				self.send_data(next_frame_to_send.val ,frame_expected.val, buffer)
				
				# /* advance sender’s upper window edge */
				next_frame_to_send.inc()

			else if n == 1 :
				# /* a data or control frame has arrived */
				
				fr = get_packet_from_physical_layer()
				# /* get incoming frame from physical layer */
				if (fr.seq == frame_expected.val) :
					# /* Frames are accepted only in order. */

					error_code =  self.network_layer.to_network_layer(fr) 
					
					if error_code == 1 :
						# Time to end transmission 
						
					# /* pass packet to network layer */
					
					# /* advance lower edge of receiver’s window */
					frame_expected.inc()
					
					# /* Ack n implies n − 1, n − 2, etc. Check for this. */
					
					while (between(ack_expected.val, fr.ack, next_frame_to_send.val)):
						# /* Handle piggybacked ack. */
						# nbuffered = nbuffered − 1 # /* one frame fewer buffered */
						nbuffered.dec()
						# /* one frame fewer buffered */
						
						stop_timer(ack_expected.val) # /* frame arrived intact # stop timer */
						
						# /* contract sender’s window */
						ack_expected.inc()

			# CheckSum error
			else if n == 2 : 
				# /* just ignore bad frames */

			# Timeout
			else if n == 3 :
				# /* trouble  retransmit all outstanding frames */
				next_frame_to_send.val = ack_expected.val
				
				# /* start retransmitting here */
				for i in range(1, nbuffered.val + 1):
					
					self.send_data(next_frame_to_send, frame_expected.val, buffer)
					#/* resend frame */
					next_frame_to_send.inc()
					# /* prepare to send the next one */
			else : 
				print("outside precribed event type ")

			if (nbuffered.val < self.MAX_SEQ):
				self.networkLayer.enable()
			else:
				self.networkLayer.disable()

		## WHILE TRUE ENDS