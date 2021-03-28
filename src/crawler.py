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


def crawl(pages, WebUrl):
	if (pages > 0) :
		print("We shall go to " + str(pages-1) + " more levels of these pages")

	
		url = WebUrl
		code = requests.get(url)
		plain = code.text

		s = BeautifulSoup(plain, "html.parser")

		child_url_list = []
		for link in s.findAll('a'):
			child_url = link.get('href')

			if(validate_url(child_url)):
				print(child_url)
				child_url_list.append(child_url)

		for child in child_url_list:
			crawl(pages-1, child)
	else:
		return




crawl(2, "https://www.google.com")
print("Crawling has ended")