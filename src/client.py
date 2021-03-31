import socket 
import sys
import time
from queue import Queue

# IP = '192.168.91.201'
PORT = 49664
FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
SIZE = 2048





def run_client(IP = socket.gethostbyname(socket.gethostname())):

	ADDR = (IP, PORT)

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client.connect(ADDR)

		print(f"[CONNECTED] Client connected to server at {IP} : {PORT} ")

		# for command in list_of_commands:
		# 	client.send(command.encode(FORMAT))
			# print(f"[WAITING FOR ] {command}")
			
			response = client.recv(SIZE).decode(FORMAT)
			print(f"[RESPONSE] {response}")
			# time.sleep(1)
	except:
		print(f"No connection with {ADDR} ")

# get the input.txt path
# send that path to the run_client function
if __name__=='__main__':
	if len(sys.argv) == 2:
		run_client(sys.argv[1])
	else:
		run_client()



