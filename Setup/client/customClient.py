from socket import *
import sys # In order to terminate the program
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import hashlib

setdefaulttimeout(3)


def sendVuln(user, password, fingerprint, description):
	#create an INET, STREAMing socket
	clientSocket = socket(AF_INET, SOCK_STREAM)
	# bind the socket to a public host, and a well-known port
	clientSocket.connect(('192.168.50.10', 4347))


	#SEND REQUEST
	clientSocket.send(b"NEW_CONNEC")

	#RECEIVE CERTIFICATE
	message = clientSocket.recv(4096)
	if (message[:10].decode() != "CRT_SEND.."):
		print("Error receiving the certificate")
		return -1
	cert = x509.load_pem_x509_certificate(message[10:], default_backend())
	public_key = cert.public_key()


	#GENERATE SYMMETRIC KEY
	symKey = Fernet.generate_key()
	f = Fernet(symKey)

	#SEND SYMMETRIC KEY
	message = public_key.encrypt(symKey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
	clientSocket.send(b"SYM_SEND.." + message)



	#RECEIVE SYMKEY ACK
	message = clientSocket.recv(4096)
	if (message[:10].decode() != "SYM_ACK..."):
		print("Error receiving the symkey ack")
		return -2

	message = f.decrypt(message[10:])
	if (message.decode() != "SYM_ACK2.."):
		print("Error receiving the symkey ack")
		return -3


	#SEND LOGIN REQUEST
	message = "user:"+user+";pass:"+password+";"
	message = message.encode()
	token = f.encrypt(message)
	clientSocket.send(b"LOG_REQUES" + token)


	#RECEIVE LOGIN RESPONSE
	message = clientSocket.recv(4096)
	if (message[:10].decode() == "LOG_WUSER."):
		print("User not found")
		return -4

	if (message[:10].decode() == "LOG_WPASS."):
		print("Wrong password")
		return -5

	if (message[:10].decode() != "LOG_CORREC" or f.decrypt(message[10:]).decode() != ("LOG_CORRE2"+user)):
		print("Error making login")
		return -6


	#SEND VULNERABILITY
	message = "fing:"+fingerprint + ";desc:"+description+";"
	import hashlib
	hash_object = hashlib.sha256(message.encode())
	message += "hash:"+hash_object.hexdigest()+";"
	message = message.encode()
	token = f.encrypt(message)
	clientSocket.send(b"VUL_SUBMIT" + token)

	#RECEIVE VULN RESPONSE
	message = clientSocket.recv(4096)
	if (message[:10].decode() == "VUL_DUPLIC"):
		print("This vulnerability was already submitted for user "+ user + ", exiting.")
		return -7

	if (message[:10].decode() == "VUL_ERROR."):
		print("Error submitting submitting vulnerability")
		return -8

	if (message[:10].decode() == "VUL_HASHER"):
		print("Error submitting submitting vulnerability: Hashes don't match")
		return -9

	if (message[:10].decode() != "VUL_ACCEPT"):
		print("Error submitting submitting vulnerability")
		return -9

	msg = f.decrypt(message[10:]).decode()
	l1 = msg.split("points:")

	print("Vulnerability submitted, you ("+user+") have now "+l1[1]+" points.\n")
	return 0