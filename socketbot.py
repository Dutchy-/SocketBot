#!/usr/bin/python2
import irclib
import socket
import threading
import os
import os.path

import signal
import sys

# Constants
socketdir = 'channels'

# Connection information
network = 'irc.snt.utwente.nl'
port = 6667
channels = ['#socketbot', '#iapps']
nick = 'SocketBot'
name = 'Dutchy'

# Create an IRC object
irc = irclib.IRC()

class ClientHandler(threading.Thread):
	def __init__(self, sock, addr):
		super( ClientHandler, self).__init__()
		self.sock = sock
		self.addr = addr

	def run(self):
		line = self.sock.recv(1024)
	 	while line:
			server.privmsg(os.path.basename(self.sock.getsockname()), line)
			line = self.sock.recv(1024)


class SocketListener(threading.Thread):
	def __init__(self, ssock):
		super( SocketListener, self ).__init__()
		self.daemon = True
		self.ssock = ssock
	
	def run(self):
		while True:
			sock, addr = self.ssock.accept()
			ClientHandler(sock, addr).start()

def init_sockets(channels):
	sockets = {}
	try:
		os.makedirs(socketdir)
	except OSError:
		# Maybe in the future we really need to check for writability and such
		pass
	for channel in channels:
		path = os.path.join(socketdir, channel)
		try:
			os.remove(path)
		except OSError:
			# We really should just continue
			pass
		# Create a unix socket and bind to it
		s = socket.socket(socket.AF_UNIX)
		s.bind(path)
		# Start the listeners
		s.listen(1)
		SocketListener(s).start()
		sockets[channel] = s
	return sockets

def init_server(network, port, nick, ircname, channels):
	server = irc.server()
	server.connect(network, port, nick, ircname)
	for channel in channels:
		server.join(channel)
	return server

# Get channel -> unix socket dict
sockets = init_sockets(channels)
# Join the server
server = init_server(network, port, nick, name, channels)
# Before we start looping, make a signal handler
def shutdown(signal, frame):
	server.disconnect()
	sys.exit(0)
signal.signal(signal.SIGINT, shutdown)
# Jump into an infinite loop
irc.process_forever()
