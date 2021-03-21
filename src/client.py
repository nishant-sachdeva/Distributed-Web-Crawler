import socket 
import sys
import time
from queue import Queue

# IP = '192.168.91.201'
PORT = 49664
FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
SIZE = 2048





def run_client(input_filepath , IP = socket.gethostbyname(socket.gethostname())):

	ADDR = (IP, PORT)

	with open(input_filepath) as fl:
		list_of_commands = [x.rstrip() for x in fl]

	# for command in list_of_commands:
	# 	print(command)

	list_of_commands.append(DISCONNECT_MSG)


	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client.connect(ADDR)

		print(f"[CONNECTED] Client connected to server at {IP} : {PORT} ")

		for command in list_of_commands:
			client.send(command.encode(FORMAT))
			print(f"[SENDING] {command}")
			
			response = client.recv(SIZE).decode(FORMAT)
			print(f"[RESPONSE] {response}")
			# time.sleep(1)
	except:
		print(f"Could not connect to {ADDR} ")

# get the input.txt path
# send that path to the run_client function
if __name__=='__main__':
	if len(sys.argv) == 3:
		run_client(sys.argv[1], sys.argv[2])
	else:
		run_client(sys.argv[1])



