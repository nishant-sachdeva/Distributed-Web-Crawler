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
def execute_commands():
	# the idea is to check if the queue has any elements
	# if yes, then pop one and execute
	while True:
		received_command = False
		
		with data_lock:
			if not command_queue.empty():
				command_object = command_queue.get()
				received_command = True
		

		# because I want to keep the processing out of the data lock
		if received_command == True:		
			connection_object = command_object["connection"]
			address = str(command_object["address"])
			command = str(command_object["command"])

			print(f"[{address}] {command} ")

			if command == DISCONNECT_MSG:
				print(f"[CLOSING] Terminating Connnection with {address}")
				connection_object.close()
			
			else:
				result = run_command(command)
				connection_object.send(result.encode(FORMAT))
		else:
			time.sleep(1)

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

	ADDR = ('', PORT)
	print("[STARTING] Server is starting ...")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)
	server.listen()

	print(f"[LISTENING] Server is listening on {IP}:{PORT}" )
	

	# now, we start waiting for clients
	thread_execute_commands = threading.Thread(target = execute_commands)
	thread_execute_commands.start()

	while True:
		connection, address = server.accept()
		thread_receive_commands = threading.Thread(target = handle_client, args = (connection, address) )
		thread_receive_commands.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2} ")


if __name__=='__main__':
	if len(sys.argv) == 2:
		start_server(sys.argv[1])
	else:
		start_server()
