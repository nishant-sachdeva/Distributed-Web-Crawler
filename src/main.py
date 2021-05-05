import json
import random
import requests

from generate_urls import make_urls, get_random_url

# number_of_ports = int(input("Enter number of ports : "))
number_of_ports = 4
URLS = make_urls(number_of_ports)

print(URLS)

gateway_storage_dict = {}


while True:
	command = input("=> Enter Command : ")

	if command == "end":
		break
	elif command == "crawl":
		website = input("Enter Website : ")
		levels = int(input("Enter levels : "))
		
		#choose any random url
		[random_index, random_url] = get_random_url(URLS)
		# this url is of the format : http://localhost::5000/ 
		# now we need to add "crawl" in it
		
		url = random_url + "crawl"

		params = {
			'website' : website,
			'levels' : levels,
		}
		try:
			r = requests.get(url=url, params = params)
			print("Crawling has returned. Better sign")
			print(r.text)
			# if r.text == "ok":
			# 	print("Crawling complete")
			# else:
			# print("Crawling experienced some issues. Debug to find out")
		except:
			print("Crawling operation did not exist")
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

	