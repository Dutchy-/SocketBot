#!/usr/bin/python2
# Tool to connect to a SocketBot unix socket
import sys

def print_help():
	print("Usage: ./connect.py <channel>")

def connect():
	import os.path
	import socketbot
	import socket
	socket_path = os.path.join(socketbot.socketdir, os.path.basename(sys.argv[1]))
	s = socket.socket(socket.AF_UNIX)
	s.connect(socket_path)
	try:
		while True:
			s.send(sys.stdin.readline())
	except KeyboardInterrupt:
		print("Ctrl-C received, disconnecting")


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print_help()
	else:
		try: 
			connect()
		except IOError:
			print("Connection problem, are you sure SocketBot is running for {0}?".format(sys.argv[1]))



