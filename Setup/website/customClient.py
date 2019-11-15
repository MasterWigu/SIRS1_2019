from socket import *
import sys # In order to terminate the program
from cryptography import x509
from cryptography.hazmat.backends import default_backend


#create an INET, STREAMing socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to a public host, and a well-known port
clientSocket.connect(('127.0.0.1', 4343))

clientSocket.send(b"NEW_CONNECTION")


message = clientSocket.recv(4096)
cert = x509.load_pem_x509_certificate(message, default_backend())

print("\n\n\n\n\n")
print(cert.public_key())

print("\n\n\n\n\n")
print(cert)


print("\n\n\n\n\n")