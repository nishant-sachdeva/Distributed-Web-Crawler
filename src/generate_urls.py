def make_urls(number_of_ports):
	URLS = []
	for i in range(number_of_ports):
		url = "http://localhost:" + str(5000+i) + "/"
		URLS.append(url)

	return URLS
	URLS = []