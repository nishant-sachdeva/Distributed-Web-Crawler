import requests
from bs4 import BeautifulSoup
import validators

import networkx as nx

def validate_url(url):
	try:
		if validators.url(url):
			return True
		return False
	except:
		return False

def hard_disk_store(text, url):
	name = "storage/" + url.replace('/', '') + ".txt" 
	print("html stored in ", name)
	file = open(name,"w+")
	file.write(text)
	file.close()

	return


def crawl(WebUrl):
	print("inside crawling now")

	code = requests.get(url=WebUrl)
	plain = code.text

	hard_disk_store(plain, WebUrl)

	s = BeautifulSoup(plain, "html.parser")

	child_url_list = []
	for link in s.findAll('a'):
		child_url = link.get('href')

		if(validate_url(child_url)):
			# print(child_url)
			child_url_list.append(child_url)

	return child_url_list

# crawl('https://nishant-sachdeva.github.io/')