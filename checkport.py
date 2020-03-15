# _*_ coding:utf-8 _*_

import socket
import logging
import time
import telnetlib

logging.basicConfig(level = logging.INFO,format = '[%(asctime)s] - [%(levelname)s] %(message)s',filename='/data/logs/checkport.log')

def check_port(ip,port):
    #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        struct_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #server=telnetlib.Telnet()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.connect((ip,port))
            #print '[%s] %s port %s is open' %(struct_time,ip,port)
            logging.info('%s port %s is open' %(ip,port))
        except Exception as err:
            #print '[%s] %s port %s is nott open' %(struct_time,ip,port)
            logging.error('%s port %s is not open' %(ip,port))
        finally:
            server.close()
        time.sleep(1)


if __name__ == "__main__":
    ip="192.168.1.10"
    port=27017
    check_port(ip,port)
