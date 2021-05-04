import requests
import json
import threading

def work():
	print("Sending requests")
	url = "http://127.0.0.1:5000/check"

	r = requests.get(url=url)

	data = r.text
	print(data)

# print(data["data"])

for i in range(100):
	x = threading.Thread(target=work)
	x.start()