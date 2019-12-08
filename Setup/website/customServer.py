from socket import *
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import bcrypt
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

with open("privatekey.pem", "rb") as key_file:
	private_key = serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend())


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 4346))
serverSocket.listen(1)

while True:
	print('The server is ready to receive')

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

		#CHECK LOGIN
		conn1 = mysql.connector.connect(host="localhost",user="root",passwd="toor",database="AVD_SCORE")

		mycursor = conn1.cursor()
		sql = "SELECT password FROM user WHERE username= %s"
		adr = (user, )
		mycursor.execute(sql, adr)
		myresult = mycursor.fetchone()
		mycursor.close()
		conn1.close()
		if myresult == None:
			print("User not found")
			message = b"LOG_WUSER."
			token = f.encrypt(b"LOG_WUSER2")
			connectionSocket.send(message + token)
			continue

		if (not bcrypt.checkpw(password.encode() , myresult[0].encode())):
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
		points = 0

		#SUBMIT VULNERABILITY IN DATABASE

		try:
			conn2 = mysql.connector.connect(host="localhost",user="root",passwd="toor",database="AVD_SCORE")
			conn2.autocommit = False
			cursor = conn2.cursor()

			sql = "SELECT points FROM user WHERE username= %s"
			adr = (user, )
			cursor.execute(sql, adr)
			myresult = cursor.fetchone()
			if myresult == None:
				print("Error")
				conn.close()
				continue
			points = myresult[0]+1
			print("CCCCC")
			sql = "UPDATE user SET points = %s WHERE username= %s"
			adr = (points, user )
			cursor.execute(sql, adr)
			print("AAAAA")
			sql = "INSERT INTO attack (fingerprint, explanation, submit_time, username)  VALUES (%s, %s, NOW(), %s)"
			adr = (fingerprint, description ,user )
			cursor.execute(sql, adr)
			print("BBB")
			#Commit your changes
			conn2.commit()

		except mysql.connector.Error as error :
			print("Failed to update record to database rollback: {}".format(error))
			#reverting changes because of exception
			conn2.rollback()
			if str(error).find("Duplicate entry") != -1:
				message = b"VUL_DUPLIC"
				token = f.encrypt(b"VUL_DUPLI2")
				connectionSocket.send(message + token)
			else:
				message = b"VUL_ERROR."
				token = f.encrypt(b"VUL_ERROR2")
				connectionSocket.send(message + token)
			continue

		finally:
			#closing database connection.
			if(conn2.is_connected()):
				#cursor.close()
				conn2.close()

		message = b"VUL_ACCEPT"
		m2 = "points:"+str(points)
		token = f.encrypt(m2.encode())
		connectionSocket.send(message + token)

		print("VULN ACCEPTED- user:" + user)



	except IOError:
			# Send HTTP response message for file not found
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			# Close the client connection socket
			connectionSocket.close()

serverSocket.close()
sys.exit()

