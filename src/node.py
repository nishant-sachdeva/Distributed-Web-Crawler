from flask import Flask, request
import threading

import requests
import sys

from crawler import crawl
from generate_urls import make_urls, get_random_url

app = Flask(__name__)

# {
#  website : [ [child, worker] , [child, worker], [child, worker] ]
#  website : [ [child, worker] , [child, worker], [child, worker] ]
#  website : [ [child, worker] , [child, worker], [child, worker] ]
#  website : [ [child, worker] , [child, worker], [child, worker] ]
# }

@app.route('/check', methods=['GET'])
def check():
	current_url = request.host
	answer = []


	for url in URLS :
		if url == current_url:
			continue
		else:
			r = requests.get(url=url)
			answer.append(r.text)

	answer_dict = {
	'answer_list' : answer,
	}

	return answer_dict



@app.route('/', methods=['GET'])
def home():
	answer = request.host
	return answer


@app.route('/crawl', methods=['GET'])
def crawler():
	print(request.host)
	if request.method == "GET":
		website = request.args.get('website')
		levels = int(request.args.get('levels'))

		# we do one layer of crawling, store in a table accordingly
		# then we send for further crawling
		# try:
		if levels > 0 :
			child_urls = crawl(website)
			# print("crawling completed " + str(request.host))

			if len(child_urls) > limiter:
					child_urls = child_urls[:limiter]

			child_worker_list = []
			for child in child_urls:
				print(levels, child)
				index , assignee = get_random_url(URLS)
				child_worker_list.append([child, assignee])

			# we have to call response for all these functions

			for child, worker in child_worker_list:
				params = {
				'website' : child,
				'levels' : levels - 1,
				}
				url = worker + "crawl"

				# try:
				r = requests.get(url = url, params = params)
				print(r.text)
			if website not in child_adjacency:
				child_adjacency[website] = child_worker_list
			else:
				# we have to append it to the existing list
				child_adjacency[website] = child_adjacency[website] + child_worker_list

		return "ok"

@app.route('/make_graph', methods=['GET'])
def make_graph():
	if request.method == "GET":
		data = request.args.get('command')

		answer = {
		'data' : data + " has been received",
		}

	return answer



URLS = []

number_of_ports = 4

limiter = 5

child_adjacency = {}


if __name__ == '__main__':
	try:
		port_number = int(sys.argv[1])
		print(port_number)
	except:
		print("Enter port number please")
		exit(0)

	URLS = make_urls(number_of_ports)
		
	print("starting server at port " + str(port_number))

	app.run(port=port_number, threaded=True, debug=True)


