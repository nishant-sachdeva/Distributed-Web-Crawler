def check_if_exists_and_print_html(name):
	try:
		f = open(name, 'r')
		Lines = f.readlines()
		for line in Lines:
			print(line)
		f.close()
	except IOError:
		print("File not accessible")
	return