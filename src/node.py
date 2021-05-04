from flask import Flask, request
import threading

import requests

from generate_urls import make_urls

app = Flask(__name__)

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
def crawl():
	if request.method == "GET":
		data = request.args.get('command')

		answer = {
		'data' : data + " has been received",
		}

	return answer


@app.route('/make_graph', methods=['GET'])
def make_graph():
	if request.method == "GET":
		data = request.args.get('command')

		answer = {
		'data' : data + " has been received",
		}

	return answer


def startapp(port_number):
	print("starting server at port " + str(port_number))
	app.run(port=port_number, threaded=True)

URLS = []

if __name__ == '__main__':
	number_of_ports = int(input("Enter number of ports: "))
	URLS = make_urls(number_of_ports)

	for i in range(number_of_ports):
		thread = threading.Thread(target=startapp, args=(5000+i, ))
		thread.start()


