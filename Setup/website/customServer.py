from socket import *
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import bcrypt

with open("privatekey.pem", "rb") as key_file:
	private_key = serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend())

mydb = mysql.connector.connect(host="localhost",user="root",passwd="toor",database="AVD_SCORE")

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 4343))
serverSocket.listen(100)

n=0
while n<1:
	print('The server is ready to receive')

	n=3
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()


	try:
		#RECEIVE REQUEST
		message = connectionSocket.recv(4096).decode()
		if (message != "NEW_CONNEC"):
			continue


		#SEND CERTIFICATE
		crt = open("server.crt", 'rb')
		connectionSocket.send("CRT_SEND..".encode() + crt.read())



		#RECEIVE SYMMETRIC KEY
		message = connectionSocket.recv(4096)
		if (message[:10].decode() != "SYM_SEND.."):
			continue
		symKey = private_key.decrypt(message[10:], padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
		

		#SEND SYMKEY ACK
		message = b"SYM_ACK..."
		f = Fernet(symKey)
		token = f.encrypt(b"SYM_ACK2..")
		connectionSocket.send(message + token)


		#RECEIVE LOGIN REQUEST
		message = connectionSocket.recv(4096)
		if (message[:10].decode() != "LOG_REQUES"):
			continue
		message = f.decrypt(message[10:])
		message = message.decode()
		s1 = message.replace("user:", "").replace("pass:", "").split(";")
		user = s1[0]
		password = s1[1]


		print("\n\n"+str(s1)+"\n\n")

		#CHECK LOGIN
		mycursor = mydb.cursor()
		sql = "SELECT password FROM user WHERE username= %s"
		adr = (user, )
		mycursor.execute(sql, adr)
		myresult = mycursor.fetchone()
		if myresult == None:
			print("User not found")
			message = b"LOG_WUSER."
			token = f.encrypt(b"LOG_WUSER2")
			connectionSocket.send(message + token)
			continue

		if (not bcrypt.checkpw(password.encode() , myresult[0].encode()):
			print("Wrong password")
			message = b"LOG_WPASS."
			token = f.encrypt(b"LOG_WPASS2")
			connectionSocket.send(message + token)
			continue

		#SEND LOGIN RESPONSE
		message = b"LOG_CORREC"
		m2 = "LOG_CORRE2"+user
		token = f.encrypt(m2.encode())
		connectionSocket.send(message + token)


		#RECEIVE VULNERABILITY
		message = connectionSocket.recv(4096)
		if (message[:10].decode() != "VUL_SUBMIT"):
			continue
		message = f.decrypt(message[10:])
		message = message.decode()
		s1 = message.replace("fing:", "").replace("desc:", "").split(";")
		fingerprint = s1[0]
		description = s1[1]


		#SUBMIT VULNERABILITY IN DATABASE



		#SEND VULN RESPONSE


		message = clientSocket.recv(4096)
		if (message[:10].decode() == "VUL_DUPLIC"):
			print("Wrong user")
			exit(-1) #TODO

		if (message[:10].decode() == "VUL_ERROR."):
			print("Wrong password")
			exit(-1) #TODO

		if (message[:10].decode() != "VUL_ACCEPT"):
			print("RIP")
			exit(-1) #TODO






	except IOError:
			# Send HTTP response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			# Close the client connection socket
			connectionSocket.close()

serverSocket.close()
sys.exit()

