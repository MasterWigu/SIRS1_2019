from socket import *
import sys

#create an INET, STREAMing socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serverSocket.bind(('', 4343))
# become a server socket
serverSocket.listen(100)


while True:
	print('The server is ready to receive')

	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()

	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(4096).decode()
		# Extract path of requested object from message
		# The Path is the second part of HTTP header,
		# identif. by [1]
		if (message != "NEW_CONNECTION"):
			continue


		crt = open("Server.crt", 'rb')
		connectionSocket.send(crt.read())




		# The extracted path of the HTTP request includes
		# a character '\', we read the path from
		# the second character
		##f = open(filename[1:])
		# Store the entire content of the requested file
		# in a temporary buffer
		##outputdata = f.read()
		# Send the HTTP response header line
		# to the connection socket
		##connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

		# Send the content of the requested file
		# to the connection socket
		'''
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode())

		# Close the client connection socket
		connectionSocket.close()
'''
	except IOError:
			# Send HTTP response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			# Close the client connection socket
			connectionSocket.close()

serverSocket.close()
sys.exit()


'''
while True:
	# accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()'''

