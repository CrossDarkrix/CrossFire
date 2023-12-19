# -*- coding: utf-8 -*-
from colorama import init as colorama_init, Fore
import socket, sys, threading
from datetime import datetime

colorama_init()

port_list = []
threads = []

def Logo():
	print(Fore.RED + """
  ___         _   ___               
 | _ \___ _ _| |_/ __| __ __ _ _ _  
 |  _/ _ \ '_|  _\__ \/ _/ _` | ' \ 
 |_| \___/_|  \__|___/\__\__,_|_||_|

          Code Customized By DarkRix""")
	print(Fore.GREEN)

class ScanThread(threading.Thread):
	def __init__(self,threadName,ip,port_start,port_end,c):
		threading.Thread.__init__(self)
		self.threadName = threadName
		self.ip = ip
		self.port_start = port_start
		self.port_end = port_end
		self.c = c

	def run(self):
		scantcp(self.threadName,self.ip,self.port_start,self.port_end,self.c)

def scantcp(threadName,ip,port_start,port_end,c):
	try :
		for port in range(port_start,port_end):
			x = port
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			socket.setdefaulttimeout(c)
			result = sock.connect_ex((ip,port))
			if result == 0:
				port_list.append(port)
			sock.close()
	except KeyboardInterrupt:
		print("Keyboard Interrupt Detected")
		sys.exit(0)	
	except socket.gaierror:
		print("Hostname coudlnt be resolved")
		sys.exit(0)
	except socket.error:
		pass
	except OverflowError:
		pass
	except:
		pass

def main():
	Logo()
	try:
		ipadress = sys.argv[1]
	except:
		try:
			ipadress = input("Target Host: ")
		except:
			ipadress = "192.168.1.0"

	print('*'*50)
	while True:
		try:
			port_start = int(input("Enter Start Ports to scan : "))
			if port_start<=0:
				continue
			else :
				break
		except ValueError:
			print("Please Enter a Valid Number")

	while True:
		try :
			port_end = int(input("Enter the End of Ports to scan : "))
			if port_end<=0:
				continue
			else :
				break
		except ValueError:
			print("Please Enter a Valid Number")

	c = 0.3
	print("*"*50)
	print('Starting scan now \n')
	t1 = datetime.now()
	print("Scan started at {}".format(t1))
	print('\nScanning the host : {}\n'.format(ipadress))
	tot_port = port_end - port_start
	tot_port_thread = 100
	tnum = tot_port / tot_port_thread

	if (tot_port % tot_port_thread != 0):
		tnum = tnum + 1
	
	try :
		for i in range(int(tnum)):
			port_end = port_start + tot_port_thread-1
			sthread = ScanThread("T1", ipadress, port_start, port_end, c)
			sthread.start()
			port_start = port_end + 1
			threads.append(sthread)
	except :
		print("Problem with starting Thread")

	for t in threads:
		t.join()

	t2 = datetime.now()	
	k = 0
	port_lists = sorted(port_list)
	for p in port_lists:
		k += 1

	print("Number Of Open Ports : {}\n".format(k))
	print("Number Of Closed/Filtered Ports : {}\n".format(tot_port - k + 1))
	print("-----------------------------------------------------------------")
	print("|\tPort\t|\tStatus\t|\tService Name      \t|")
	print("-----------------------------------------------------------------")
	for p in port_lists:
		try :
			socket.getservbyport(p)
			print("|\t{}\t|\tOPEN\t|\t{}\t|".format(p, socket.getservbyport(p)))
			print("-----------------------------------------------------------------")
		except:
			print("|\t{}\t|\tOPEN\t|\t{}\t|".format(p, "No Service Name "))
			print("-----------------------------------------------------------------")

	total = t2 - t1
	total = str(total)
	a = total.split(' ')[-1]
	x, y, z = list(map(str,a.split(':')))
	print("\nFinished scan in {} hours {} minutes {} seconds".format(x, y, z))

if __name__ == '__main__':
	main()
