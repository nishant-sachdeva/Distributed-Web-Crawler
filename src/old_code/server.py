# we want to make sure that multiple clients 
# that can can work with this system



# task 1. Sending data to an already connected client
# task 2. Listen and accept connections from other clients


# thread 1 : listen for and accept connections
# thread 2 : Sending data to an already connected client

import os
import socket 
import sys
import threading
import time
from queue import Queue

command_queue = Queue()

PORT = 49664
FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
SIZE = 2048

data_lock = threading.Lock()

graphs_dict = {}

list_of_connections = []


def run_command(command):
	# MST has been implemented

	#step 1 :: Parse the command
	#step 2 :: Perform the expected execution

	words = command.split()

	if words[0] == "crawl":
		return f"{command} :: Crawling has been done"


	elif words[0] == "show_html":
		return f"{command} :: first 100 words of the html have been displayed "

	elif words[0] == "show_graph":
		return f"{command} :: Graph has been plotted and saved with the corresponding url name "

	elif words[0] == "exit":
		os._exit(1)
	elif words[0] == "show_clients":
		with data_lock:
			for connection_object in list_of_connections:
				print("connected to " , connection_object["connection_address"] )
			print("Only so many connections are there")
	else:
		return "Bad Command. Resend"

def validate_command(command):
	words = command.split()

	if not (words[0] == "crawl" or words[0] == "show_html" or words[0] == "show_graph" or words[0] == "exit" or words[0] == "show_clients"):
		return False
	return True


# Running with thread :: thread_execute_commands
def collect_commands():
	print("Collecting commands here")
	while True:
		command = input("=> " )

		if(validate_command(command)):
			print(run_command(command))
	return

# Running with thread :: thread_receive_commands
# def handle_client(connection, address):

# 	print(f"[NEW CONNECTION] {address} connected ")
# 	connected = True

# 	while connected: 
# 		message = connection.recv(SIZE).decode(FORMAT)

# 		if message == DISCONNECT_MSG :
# 			connected = False
# 			# we shall exit the loop and leave it to the command executor to close the connections
		
# 		command = {
# 			"connection" : connection,
# 			"address" : address,
# 			"command" : message
# 		}
# 			# lock the queue, and add the command to it
# 		with data_lock:
# 			command_queue.put(command)

# 	return 


def start_server(IP = socket.gethostbyname(socket.gethostname())):
	# we shall have one thread collecting commands and one thread distributing it to the various clients

	# the default value of the address is the system's own IP address ( localhost )
	ADDR = (IP, PORT)
	print("[STARTING] Server is starting ...")

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)
	server.listen()

	print(f"[LISTENING] Server is listening for connections on {IP}:{PORT}" )
	

	# now, we start waiting for clients
	thread_collect_commands = threading.Thread(target = collect_commands)
	thread_collect_commands.start()

	while True:
		# meanwhile, we just wait for clients to connect. And when they do, we send them commands.

		connection, address = server.accept()
		
		connection_dict = {
			"connection_object" : connection,
			"connection_address" : address,
		}

		list_of_connections.append(connection_dict)

		# thread_send_commands = threading.Thread(target = handle_client, args = (connection, address) )
		
		# thread_send_commands.start()
		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2} ")


# the argument here is the IP address for the server 
# for now, we are keeping it as the system IP address ( or the localhost ) cuz we just need proof of concept

if __name__=='__main__':
	if len(sys.argv) == 2:
		# this means an artificial IP address has been provided
		start_server(sys.argv[1])
	else:
		start_server()
