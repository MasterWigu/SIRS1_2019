import importlib
from customClient import *
from time import sleep


print("Input angr launch file: ")
fName = str(input())
try:
	file = importlib.import_module(fName)
except ModuleNotFoundError:
	print("The file '"+fName+"' was not found. Exiting.\n")
	exit(-1)

print("Opening file '"+fName+"'.\n")
print("Running main().\n")
finger = file.main()


print("Fingerprint is: '"+ finger + "'. Submit? [Y/n]")
while 1:
	choice = str(input())
	if choice.lower() == "n":
		print("Are you sure you want to discard? [N/y]")
		while 1:
			choice = str(input())
			if choice.lower() == "n":
				break
			if choice.lower() == "y":
				print("Exiting.\n")
				exit(0)
			print("Are you sure you want to discard? [N/y]")
	elif choice.lower() == "y":
		break
	print("Fingerprint is: '"+ finger + "'. Submit? [Y/n]")

print("\nEnter the description of the vulnerability:\n")
desc = str(input())


print("Enter your username: ")
user = str(input())
print("Enter your password: ")
password = str(input())

while 1:
	succ = sendVuln(user, password, finger,desc)
	if succ == -1 or  succ == -2 or  succ == -3 or  succ == -6 or  succ == -8 or  succ == -9:
		print("Detected errors trying to submit vulnerability. Trying again in 3 seconds.\n")
		sleep(3)
	elif succ == -4 or succ == -5:
		print("Please input your username and password again.\n")
		print("Enter your username: ")
		user = str(input())
		print("Enter your password: ")
		password = str(input())
	else:
		break

