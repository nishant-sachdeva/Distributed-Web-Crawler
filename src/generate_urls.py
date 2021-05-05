import random

def make_urls(number_of_ports):
	URLS = []
	for i in range(number_of_ports):
		url = "http://localhost:" + str(5000+i) + "/"
		URLS.append(url)

	return URLS
	URLS = []


def get_random_url(list_of_urls):
	random_index = random.randint(0, len(list_of_urls)-1)
	random_url = list_of_urls[random_index]

	return [random_index, random_url]