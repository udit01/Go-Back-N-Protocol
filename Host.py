#!/usr/bin/python

import os
import sys
import socket
# from threading import Thread
from Node import *
import argparse

class Host():
	"""
	HOST running Go-Back-N protocol for reliable data transfer.
	Both sender and receiever
	"""
	def __init__(self,
				ip="127.0.0.1",
				port=3000,
				infilepath=os.path.join(os.getcwd(), "a.txt"),
				outfilepath=os.path.join(os.getcwd(), "b.txt")):
		# WWW is the data path
		self.node = Node(ip=ip, port=port, infilepath=infilepath, outfilepath=outfilepath)


# if __name__ == "__main__":
#     # Argument parser
#     parser = argparse.ArgumentParser(description='Go-Back-N Protocol Server Application',
#                                      prog='python \
#                                            ServerApp.py \
#                                            -f <filename> \
#                                            -a <sender_ip> \
#                                            -b <sender_port> \
#                                            -x <receiver_ip> \
#                                            -y <receiver_port> \
#                                            -m <sequence_number_bits> \
#                                            -t <timeout> \
#                                            -w <www>')
#     parser.add_argument("-f", "--filename", type=str, default="index.html",
#                         help="File to be received, default: index.html")
#     parser.add_argument("-a", "--sender_ip", type=str, default="127.0.0.1",
#                         help="Sender IP, default: 127.0.0.1")
#     parser.add_argument("-b", "--sender_port", type=int, default=8081,
#                         help="Sender Port, default: 8081")
#     parser.add_argument("-x", "--receiver_ip", type=str, default="127.0.0.1",
#                         help="Receiver IP, default: 127.0.0.1")
#     parser.add_argument("-y", "--receiver_port", type=int, default=8080,
#                         help="Receiver Port, default: 8080")
#     parser.add_argument("-m", "--sequence_number_bits", type=int, default=2,
#                         help="Total number of bits used in sequence numbers, default: 2")
#     parser.add_argument("-t", "--timeout", type=int, default=10,
#                         help="Timeout, default: 10")
#     parser.add_argument("-w", "--www", type=str, default=os.path.join(os.getcwd(), "data", "receiver"),
#                         help="Destination folder for receipt, default: /<Current Working Directory>/data/receiver/")

#     # Read user inputs
#     args = vars(parser.parse_args())

#     # Run Server Application
#     ServerApp(**args)



if __name__ == "__main__":
	# Argument parser
	parser = argparse.ArgumentParser(description='Go-Back-N Protocol Client Application',
									 prog='python \
										   ClientApp.py \
										   -inf <in_filename> \
										   -of <out_filename> \
										   -i <ip> \
										   -p <port>')
										#     \
										#    -w <window_size> \
										#    -s <max_segment_size> \
										#    -n <total_packets> \
										#    -t <timeout> \
										#    -d <www>')

	parser.add_argument("-inf", "--infilename", type=str, default="a.txt", dest='inf',
						help="File to be sent, default: a.txt")
	parser.add_argument("-of", "--ofilename", type=str, default="b.txt", dest='of',
						help="File to be sent, default: b.txt")
	
	parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", dest='i',
						help="IP, default: 127.0.0.1")
	parser.add_argument("-p", "--port", type=int, default=5000, dest='p',
						help="Port, default: 5000")

	# parser.add_argument("-m", "--sequence_number_bits", type=int, default=2,
	#                     help="Total number of bits used in sequence numbers, default: 2")
	# parser.add_argument("-w", "--window_size", type=int, default=3,
	#                     help="Window size, default: 3")
	# parser.add_argument("-s", "--max_segment_size", type=int, default=1500,
	#                     help="Maximum segment size, default: 1500")
	# parser.add_argument("-n", "--total_packets", type=str, default="ALL",
	#                     help="Total packets to be transmitted, default: ALL")
	# parser.add_argument("-t", "--timeout", type=int, default=10,
	#                     help="Timeout, default: 10")
	# parser.add_argument("-d", "--www", type=str, default=os.path.join(os.getcwd(), "data", "sender"),
	#                     help="Source folder for transmission, default: /<Current Working Directory>/data/sender/")

	# Read user inputs
	args = (parser.parse_args())

	# Run Client Application
	Host(args.i, args.p, args.inf, args.of)
