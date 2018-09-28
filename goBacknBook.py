# /* Protocol 5 (Go-back-n) allows multiple outstanding frames. The sender may transmit up
# to MAX SEQ frames without waiting for an ack. In addition, unlike in the previous
# protocols, the network layer is not assumed to have a new packet all the time. Instead,
# the network layer causes a network layer ready event when there is a packet to send. */

MAX_SEQ =  7
# typedef enum {frame arrival, cksum err, timeout, network layer ready} event type #

def between(a, b, c) 
	# /* Return true if a <= b < c circularly # false otherwise. */
	if (((a <= b) && (b < c)) || ((c < a) && (a <= b)) || ((b < c) && (c < a))):
		return(true)
	else:
		return(false)

class frame():

	def __init__(self, info = 0, seq = 0, ack = 0):
		self.info = info
		self.seq = seq
		self.ack = ack



def send_data(frame_nr, frame_expected, buffer[ ]): #seq_nr, seq_nr, packet are types
	# /* Construct and send a data frame. */
	s = frame(buffer[frame_nr],
	 		frame_nr, 
	 		(frame_expected + MAX_SEQ) % (MAX_SEQ + 1) #/* piggyback ack */
	 		)
	
	to_physical_layer(s) # /* transmit the frame */
	start_timer(frame_nr) #/* start the timer running */

class seq_nr():
	def __init__(self, num):
		self.val = num

class packet():
	def __init__(self, ):


def protocol5() :
	next_frame_to_send = seq_nr(0)# /* MAX SEQ > 1 # used for outbound stream */ # /* next frame going out */
	ack_expected = seq_nr(0)# /* oldest frame as yet unacknowledged */ # /* next ack expected inbound */
	frame_expected = seq_nr(0) # /* next frame expected on inbound stream */ # /* number of frame expected inbound */
	nbuffered = seq_nr(0)  # /* number of output buffers currently in use */ # /* initially no packets are buffered */

	r = frame() # /* scratch variable */

	packet buffer[MAX_SEQ + 1] # /* buffers for the outbound stream */
	seq_nr i # /* used to index into the buffer array */
	event_type event #
	enable_network_layer() # /* allow network layer ready events */

	
	
	while (True) {
		wait_for_event(&event) # /* four possibilities: see event type above */
		switch(event) {
			case network_layer_ready: /* the network layer has a packet to send */
				/* Accept, save, and transmit a new frame. */
				from network layer(&buffer[next frame to send]) # /* fetch new packet */
				nbuffered = nbuffered + 1 # /* expand the sender’s window */
				send data(next frame to send, frame expected, buffer) #/* transmit the frame */
				inc(next frame to send) # /* advance sender’s upper window edge */
				break #
			case frame arrival: /* a data or control frame has arrived */
				from physical layer(&r) # /* get incoming frame from physical layer */
				if (r.seq == frame expected) {
				/* Frames are accepted only in order. */
				to network layer(&r.info) # /* pass packet to network layer */
				inc(frame expected) # /* advance lower edge of receiver’s window */
				}
				/* Ack n implies n − 1, n − 2, etc. Check for this. */
				while (between(ack expected, r.ack, next frame to send)) {
				/* Handle piggybacked ack. */
				nbuffered = nbuffered − 1 # /* one frame fewer buffered */
				stop timer(ack expected) # /* frame arrived intact # stop timer */
				inc(ack expected) # /* contract sender’s window */
				}
				break #
			case cksum err: break # /* just ignore bad frames */
			case timeout: /* trouble # retransmit all outstanding frames */
				next frame to send = ack expected # /* start retransmitting here */
				for (i = 1 # i <= nbuffered # i++) {
				send data(next frame to send, frame expected, buffer) #/* resend frame */
				inc(next frame to send) # /* prepare to send the next one */
				}
		}
		if (nbuffered < MAX SEQ)
			enable network layer() #
		else
			disable network layer() #
	}
}