from socket import *
import threading
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
from time import strftime
import hashlib





with open("privatekey.pem", "rb") as key_file:
	private_key = serialization.load_pem_private_key(key_file.read(),password=None,backend=default_backend())




serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 4347))
serverSocket.listen(10)
setdefaulttimeout(2)

def new_client(clientSock, addr):
	try:
		logFile = open("customServer.log", "a+")
		logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " INFO: New connection started\n")
		logFile.close()
		#RECEIVE REQUEST
		message = clientSock.recv(4096).decode()
		if (message != "NEW_CONNEC"):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Wrong packet recieved, expected 'NEW_CONNEC'\n")
			logFile.close()
			return


		#SEND CERTIFICATE
		crt = open("server.crt", 'rb')
		clientSock.send("CRT_SEND..".encode() + crt.read())



		#RECEIVE SYMMETRIC KEY
		message = clientSock.recv(4096)
		if (message[:10].decode() != "SYM_SEND.."):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Wrong packet recieved, expected 'SYM_SEND'\n")
			logFile.close()
			return
		symKey = private_key.decrypt(message[10:], padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
		

		#SEND SYMKEY ACK
		message = b"SYM_ACK..."
		f = Fernet(symKey)
		token = f.encrypt(b"SYM_ACK2..")
		clientSock.send(message + token)

		#RECEIVE LOGIN REQUEST
		message = clientSock.recv(4096)
		if (message[:10].decode() != "LOG_REQUES"):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Wrong packet recieved, expected 'LOG_REQUES'\n")
			logFile.close()
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
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " WARN: User not found trying to login\n")
			logFile.close()
			print("User not found")
			message = b"LOG_WUSER."
			token = f.encrypt(b"LOG_WUSER2")
			clientSock.send(message + token)
			return

		if (not bcrypt.checkpw(password.encode() , myresult[0].encode())):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " WARN: Incorrect password while trying to login\n")
			logFile.close()
			print("Wrong password")
			message = b"LOG_WPASS."
			token = f.encrypt(b"LOG_WPASS2")
			clientSock.send(message + token)
			return

		#SEND LOGIN RESPONSE
		message = b"LOG_CORREC"
		m2 = "LOG_CORRE2"+user
		token = f.encrypt(m2.encode())
		clientSock.send(message + token)

		#RECEIVE VULNERABILITY
		message = clientSock.recv(4096)
		if (message[:10].decode() != "VUL_SUBMIT"):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Wrong packet recieved, expected 'VUL_SUBMIT'\n")
			logFile.close()
			return
		message = f.decrypt(message[10:])
		message = message.decode()
		s1 = message.replace("fing:", "").replace("desc:", "").replace("hash:", "").split(";")
		fingerprint = s1[0]
		description = s1[1]
		mhash = s1[2]
		mr = "fing:"+fingerprint + ";desc:"+description+";"
		if (mhash != hashlib.sha256(mr.encode()).hexdigest()):
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Wrong hash recieved when receiving vulnerability\n")
			logFile.close()
			message = b"VUL_HASHER"
			token = f.encrypt(b"VUL_HASHER")
			clientSock.send(message + token)
			return


		#SUBMIT VULNERABILITY IN DATABASE
		points = 0
		try:
			conn2 = mysql.connector.connect(host="localhost",user="root",passwd="toor",database="AVD_SCORE")
			conn2.autocommit = False
			cursor = conn2.cursor()

			sql = "SELECT points FROM user WHERE username= %s"
			adr = (user, )
			cursor.execute(sql, adr)
			myresult = cursor.fetchone()
			if myresult == None:
				logFile = open("customServer.log", "a+")
				logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Error trying to fetch user points: no user returned\n")
				logFile.close()
				conn.close()
				return
			points = myresult[0]+1
			sql = "UPDATE user SET points = %s WHERE username= %s"
			adr = (points, user )
			cursor.execute(sql, adr)
			sql = "INSERT INTO attack (fingerprint, explanation, submit_time, username)  VALUES (%s, %s, NOW(), %s)"
			adr = (fingerprint, description ,user )
			cursor.execute(sql, adr)
			#Commit your changes
			conn2.commit()

		except mysql.connector.Error as error :
			print("Failed to update record to database rollback: {}".format(error))
			#reverting changes because of exception
			conn2.rollback()
			if str(error).find("Duplicate entry") != -1:
				message = b"VUL_DUPLIC"
				token = f.encrypt(b"VUL_DUPLI2")
				clientSock.send(message + token)
				logFile = open("customServer.log", "a+")
				logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " WARN: Trying to submit duplicate vulnerability\n")
				logFile.close()
			else:
				message = b"VUL_ERROR."
				token = f.encrypt(b"VUL_ERROR2")
				clientSock.send(message + token)
				logFile = open("customServer.log", "a+")
				logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Error trying to submit vulnerability\n")
				logFile.close()
			return

		finally:
			#closing database connection.
			if(conn2.is_connected()):
				#cursor.close()
				conn2.close()

		message = b"VUL_ACCEPT"
		m2 = "points:"+str(points)
		token = f.encrypt(m2.encode())
		clientSock.send(message + token)

		logFile = open("customServer.log", "a+")
		logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " INFO: Vulnerability accepted - user: "+user+"\n")
		logFile.close()
		print("VULN ACCEPTED- user:" + user)



	except IOError:
			logFile = open("customServer.log", "a+")
			logFile.write(strftime("%Y/%m/%d %H:%M:%S")+ " ERROR: Socket communication error\n")
			logFile.close()
			# Send HTTP response message for file not found
			clientSock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
			# Close the client connection socket
			clientSock.close()


while True:
	print('The server is ready to receive')

	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()

	thread = threading.Thread(target = new_client, args = (connectionSocket, addr))
	thread.start()

	

serverSocket.close()
sys.exit()

