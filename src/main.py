import json
import requests

from generate_urls import make_urls

number_of_ports = int(input("Enter number of ports : "))
URLS = make_urls(number_of_ports)

while True:
	command = input("=> Enter Command : ")

	if command == "end":
		break
	elif command == "crawl":
		website = input("Enter Website : ")
		levels = int(input("Enter levels : "))
		
		#choose any random url
		# send crawl request
		# get response
		# print response

		continue
	elif command == "make_graph":
		website = input("Enter Website : ")
		levels = int(input("Enter levels : "))

		# choose any random url
		# send crawl request
		# get response
		# print response
		continue
	elif command == "show_html":
		website = input("Enter Website : ")

		# check if file exists if yes, print it
		continue
	else:
		print("Invalid Command . Try Again")
		continue

	