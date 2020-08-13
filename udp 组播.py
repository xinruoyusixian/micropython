
import socket 
import time
dst = ('224.0.0.251', 5353) 
#dst = ('255.255.255.255', 5353)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
s.sendto(b'10036',dst)  
