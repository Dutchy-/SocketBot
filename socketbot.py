#!/usr/bin/python2
import irclib
import socket
import threading
import os

import signal
import sys


os.remove('./socket')

unix = socket.socket(socket.AF_UNIX)

unix.bind('./socket')
unix.listen(1)

# Connection information
network = 'irc.snt.utwente.nl'
port = 6667
channel = '#inter-actief'
nick = 'SocketBot'
name = 'Python Test'

# Create an IRC object
irc = irclib.IRC()

# Create a server object, connect and join the channel
server = irc.server()
server.connect ( network, port, nick, ircname = name )
server.join ( channel )

class ClientHandler(threading.Thread):
	def __init__(self, sock, addr):
		super( ClientHandler, self).__init__()
		self.sock = sock
		self.addr = addr

	def run(self):
		line = self.sock.recv(1024)
	 	while line:
			server.privmsg('#inter-actief', line)
			line = self.sock.recv(1024)


class SocketListener(threading.Thread):
	def run(self):
		while True:
			sock, addr = unix.accept()
			ClientHandler(sock, addr).start()
			print("accepted connection")

socklist = SocketListener()
socklist.daemon = True
socklist.start()
#exit(0)
def shutdown(signal, frame):
	server.disconnect()
	print("Shutdown!")
	sys.exit(0)

signal.signal(signal.SIGINT, shutdown)


# Jump into an infinite loop
irc.process_forever()
