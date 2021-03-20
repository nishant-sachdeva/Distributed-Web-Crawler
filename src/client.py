import xmlrpc.client

with xmlrpc.client.ServerProxy("http://10.11.1.114:8000/") as proxy:
    print("3 is even: %s" % str(proxy.is_even(3)))
    print("100 is even: %s" % str(proxy.is_even(100)))