import sys
import os

def t(t):
	for i in range(t) :
		print(" ")
if sys.argv[1]=="run":
	print("python3 run.py help to run")
if sys.argv[1]=="runinstall":
	print("pip install -r requirements.txt")
	t(10)
	os.system("pip install -r requirements.txt")
	t(10)
if sys.argv[1]=="runserver":
	if sys.argv[2]=="1":
		o = "127.0.0.1:8000"
	else:
		if sys.argv[2]=="2":
			o = "192.168.10.184:8000"
		else:
			o = sys.argv[2]
	i = "python3 manage.py runserver %s" % o
	print(i)
	t(10)
	os.system(i)
	t(10)
if sys.argv[1]=="runmig":
	print("python3 manage.py makemigrations")
	t(10)
	os.system("python3 manage.py makemigrations")
	t(10)
	print("python3 manage.py migrate")
	t(10)
	os.system("python3 manage.py migrate")
	t(10)

if sys.argv[1]=="help":
	t(2)
	print("runinstall to install pip pk")
	t(2)
	print("runserver <host>:<port> to runserver or runserver 1 to 127.0.0.1:8000 runserver or runserver 2 to 192.168.43.230:8000 runserver")
	t(2)
	print("runmig to makemigrations + migrate")
	t(2)
