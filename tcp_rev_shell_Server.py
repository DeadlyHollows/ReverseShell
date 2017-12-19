#!/usr/bin/python2.7

from random import randint
import socket
import sys

def getUserName(connection):
	user=""
	connection.send("echo $USER")
	while True:
		buff=connection.recv(1024).strip()
		if len(buff)==0:
			break
		user+=buff
	return user

def getHostName(connection):
	host=""
	connection.send("echo $HOSTNAME")
	while True:
		buff=connection.recv(1024).strip()
		if len(buff)==0:
			break
		host+=buff
	return host

def getUserHome(connection):
	home=""
	connection.send("echo $HOME")
	while True:
		buff=connection.recv(1024).strip()
		if len(buff)==0:
			break
		home+=buff
	return home

def getcwd(connection):
	connection.send("pwd")
	pwd=""
	while True:
		buff=connection.recv(1024).strip()
		if len(buff)==0:
			break
		pwd+=buff
	return pwd

def download(connection, cmd):
	cmd_split=cmd.split()

	if len(cmd_split)==1:
		print "get: missing file operand"
		print "Syntax: \n\tget <remote_file> [<local_file>]"
		sys.exit(0)

	inputFile=cmd_split[1]
	outputFile=inputFile

	if len(cmd_split)==3:
		outputFile=cmd_split[2]

	connection.send(cmd)

	fp=open(outputFile, 'wb')
	fileData=""

	while True:
		data=connection.recv(1024)
		fileData+=data
		if len(data.strip())==0:
			break

	fp.write(fileData.strip())
	fp.close()

	print "Transfer Complete ..."

def connect(ip, port):
	server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((ip, port)) # Listen on the given port ...
	server_socket.listen(1)   # Listens for a single connection ...
	connection, client_addr=server_socket.accept()
	print client_addr, "is now connected to our server at port", port

	user=getUserName(connection)
	host=getHostName(connection)
	home=getUserHome(connection)

	while True:
		pwd=getcwd(connection)
		# print pwd

		pwd=pwd.replace(home, "~")

		while True:
			cmd=raw_input("[" + user + "@" + host + " " + pwd + "]# ")
			if cmd:
				break
		# print "SENDING: ", cmd, len(cmd), "..."
		if 'exit' in cmd or 'bye' in cmd:
			connection.send(cmd)
			# print "GOT", connection.recv(1024)
			connection.close()
			break
		
		elif 'get ' in cmd:
			### For downloading purpose ...
			### Syntax:
			### get <remote_file> [<local_file>]
			download(connection, cmd)

		else:
			connection.send(cmd)
			while True:
				data=connection.recv(1024)
				print data.strip(),
				if len(data.strip())==0:
					print ""
					break

if __name__=="__main__":
	port=randint(1025, 65535)
	if len(sys.argv)==2:
		port=int(sys.argv[1])
	connect('localhost', port)