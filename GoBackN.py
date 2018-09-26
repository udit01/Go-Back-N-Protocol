# #define MAX SEQ 7
# typedef enum {frame arrival, cksum err, timeout, network layer ready} event type;
# #include "protocol.h"
# static boolean between(seq nr a, seq nr b, seq nr c)
# {
# / * Return true if a <= b < c circularly; false otherwise. * /
# if (((a <= b) && (b < c)) || ((c < a) && (a <= b)) || ((b < c) && (c < a)))
# return(true);
# else
# return(false);
# }
# static void send data(seq nr frame nr, seq nr frame expected, packet buffer[ ])
# {
# / * Construct and send a data frame. * /
# frame s;
# / * scratch variable * /
# }
# / * insert packet into frame * /
# s.info = buffer[frame nr];
# / * insert sequence number into frame * /
# s.seq = frame nr;
# s.ack = (frame expected + MAX SEQ) % (MAX SEQ + 1); / * piggyback ack * /
# / * transmit the frame * /
# to physical layer(&s);
# / * start the timer running * /
# start timer(frame nr);
# void protocol5(void)
# {
# seq nr next frame to send;
# seq nr ack expected;
# seq nr frame expected;
# frame r;
# packet buffer[MAX SEQ + 1];
# seq nr nbuffered;
# seq nr i;
# event type event;
# / * MAX SEQ > 1; used for outbound stream * /
# / * oldest frame as yet unacknowledged * /
# / * next frame expected on inbound stream * /
# / * scratch variable * /
# / * buffers for the outbound stream * /
# / * number of output buffers currently in use * /
# / * used to index into the buffer array * /
# enable network layer();
# ack expected = 0;
# next frame to send = 0;
# frame expected = 0;
# nbuffered = 0; / * allow network layer ready events * /
# / * next ack expected inbound * /
# / * next frame going out * /
# / * number of frame expected inbound * /
# / * initially no packets are buffered * /
# while (true) {
# wait for event(&event); / * four possibilities: see event type above * /SEC. 3.4
# SLIDING WINDOW PROTOCOLS
# 237
# switch(event) {
# / * the network layer has a packet to send * /
# case network layer ready:
# / * Accept, save, and transmit a new frame. * /
# from network layer(&buffer[next frame to send]); / * fetch new packet * /
# nbuffered = nbuffered + 1;
# / * expand the sender’s window * /
# send data(next frame to send, frame expected, buffer);/ * transmit the frame * /
# / * advance sender’s upper window edge * /
# inc(next frame to send);
# break;
# case frame arrival:
# from physical layer(&r);
# / * a data or control frame has arrived * /
# / * get incoming frame from physical layer * /
# if (r.seq == frame expected) {
# / * Frames are accepted only in order. * /
# / * pass packet to network layer * /
# to network layer(&r.info);
# / * advance lower edge of receiver’s window * /
# inc(frame expected);
# }
# / * Ack n implies n − 1, n − 2, etc. Check for this. * /
# while (between(ack expected, r.ack, next frame to send)) {
# / * Handle piggybacked ack. * /
# nbuffered = nbuffered − 1;
# / * one frame fewer buffered * /
# / * frame arrived intact; stop timer * /
# stop timer(ack expected);
# / * contract sender’s window * /
# inc(ack expected);
# }
# break;
# case cksum err: break;
# / * just ignore bad frames * /
# case timeout:
# / * trouble; retransmit all outstanding frames * /
# / * start retransmitting here * /
# next frame to send = ack expected;
# for (i = 1; i <= nbuffered; i++) {
# send data(next frame to send, frame expected, buffer);/ * resend frame * /
# / * prepare to send the next one * /
# inc(next frame to send);
# }
# }
# if (nbuffered < MAX SEQ)
# enable network layer();
# else
# disable network layer();
# }
# }