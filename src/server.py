# we want to make sure that multiple clients 
# that can can work with this system



# task 1. Sending data to an already connected client
# task 2. Listen and accept connections from other clients


# thread 1 : listen for and accept connections
# thread 2 : Sending data to an already connected client

import socket 
import sys
import threading
import time
from queue import Queue

import mst

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

	if words[0] == "add_graph":
		# we create a a new graph
		graph_name = words[1]
		number_of_nodes = int(words[2])
		new_graph = mst.Graph(number_of_nodes)

		with data_lock:
			graphs_dict[graph_name] = new_graph

		# we have added a new graph there
		return f"{command} :: Graph Created"


	elif words[0] == "add_edge":
		graph_name = words[1]
		vertexA = int(words[2])
		vertexB = int(words[3])
		weight = int(words[4])

		# we have to add a new edge to a graph here

		with data_lock:
			graphs_dict[graph_name].addEdge(vertexA, vertexB, weight)

		# so, we've added an edge too
		return f"{command} :: Edge added"

	elif words[0] == "get_mst":
		graph_name = words[1]

		with data_lock:
			concerned_graph = graphs_dict[graph_name]
		# we want to hold it for as less of a time as possible

		return str(concerned_graph.getMSTWeight())

	else:
		return "Bad Command. Resend"


	

# Running with thread :: thread_execute_commands
def collect_commands():
	# the idea is to collect commands from the server input and put them in a queue. 
	# then we distribute them among clients, and later we collect output

	# if yes, then pop one and execute
	while True:
		command = input("Please enter the next command => " )

		if(validate_command(command)):
			command_object = allocate_command(command, list_of_connections)
			# this should give us a dictionary with keys { command, connection_object, connection_address }
			# this tells us what client has the command been allocated to
			# the rest of the architecture has yet to be decided

		
			# with data_lock:
			# 	command_queue.push(command_object)
			

			# # because I want to keep the processing out of the data lock
			# if received_command == True:		
			# 	connection_object = command_object["connection"]
			# 	address = str(command_object["address"])
			# 	command = str(command_object["command"])

			# 	print(f"[{address}] {command} ")

			# 	if command == DISCONNECT_MSG:
			# 		print(f"[CLOSING] Terminating Connnection with {address}")
			# 		connection_object.close()
				
			# 	else:
			# 		result = run_command(command)
			# 		connection_object.send(result.encode(FORMAT))
			# else:
			# 	time.sleep(1)

	return

# Running with thread :: thread_receive_commands
def handle_client(connection, address):
	print(f"[NEW CONNECTION] {address} connected ")
	connected = True

	while connected: 
		message = connection.recv(SIZE).decode(FORMAT)

		if message == DISCONNECT_MSG :
			connected = False
			# we shall exit the loop and leave it to the command executor to close the connections
		
		command = {
			"connection" : connection,
			"address" : address,
			"command" : message
		}
			# lock the queue, and add the command to it
		with data_lock:
			command_queue.put(command)

	return 


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

		thread_send_commands = threading.Thread(target = handle_client, args = (connection, address) )
		
		thread_send_commands.start()
		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2} ")


# the argument here is the IP address for the server 
# for now, we are keeping it as the system IP address ( or the localhost ) cuz we just need proof of concept

if __name__=='__main__':
	if len(sys.argv) == 2:
		# this means an artificial IP address has been provided
		start_server(sys.argv[1])
	else:
		start_server()
