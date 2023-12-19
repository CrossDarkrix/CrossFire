# -*- coding: utf-8 -*-

import sys, socket
from time import time as ti
from math import floor
from threading import Thread

x = 1
y = 254
iPAdress = ""


try:
    iPAdress = sys.argv[1]
except:
    pass
if iPAdress == "":
    iPAdress = "192.168.1.*"

def Ping(host):
    pings = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pings.settimeout(1)
    fast_time = ti()
    try:
        pings.connect((host, 80))
    except Exception as Error:
        if '22' in str(Error) or 'argument' in str(Error):
            pass
        if 'refused' not in str(Error):
            raise(Error)
    end_time = ti()
    pings.close()

    return (end_time - fast_time) * 1000

class PingStatus(Thread):
    def __init__(self, iP_Adress):
        Thread.__init__(self)
        self.iP_Adress = iP_Adress
        self.Status = -1
    def run(self):
        try:
            self.Status = str(floor(Ping(self.iP_Adress)))
        except:
            pass

def main():
    global x, y, iPAdress
    i = int(x)
    to = int(y)
    List_of_Hosts = list()
    try:
        if (y-x) > 0:
            to = to + 1
            print("Adress to Scan: {ADEREE}".format(ADEREE=(y-x)))
            print("Ping{IPs}".format(IPs=iPAdress.replace("*","{" + str(x) + "-" + str(y) + "}")))
            for i in range(to):
                Current_iP = iPAdress.replace('*', str(i))
                PING = PingStatus(Current_iP)
                i = i + 1
                List_of_Hosts.append(PING)
                PING.start()
                
            for Hosts in List_of_Hosts:
                Hosts.join()
                if not Hosts.Status == -1:
                   print("{HOST} Responsed in {HOSTStatus}ms".format(HOST=Hosts.iP_Adress, HOSTStatus=Hosts.Status))
        else:
            pass
    except Exception as Error:
        sys.exit("There was an running the scan, propably your resources are restricted. "+str(Error))
if __name__ == "__main__":
    main()

