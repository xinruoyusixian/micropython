

#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket,network

import sys
import os
try:
    import ustruct as struct
except:
    import struct
try:
    import ubinascii as binascii
except:
    import binascii
try:
    import uhashlib as hashlib
except:
    import hashlib
    
DEBUG = False
class websocket:
    def __init__(self, s):
        self.s = s


    #发送二进制Blob    
    def write(self, data):
        l = len(data)
        if l < 126:
            # TODO: hardcoded "binary" type
            hdr = struct.pack(">BB", 0x82, l)
        else:
            hdr = struct.pack(">BBH", 0x82, 126, l)
        self.s.send(hdr)
        self.s.send(data)
    #发送文本    
    def send(self,msg,fin=True):    
        msg=msg.encode('utf-8')
        data = struct.pack('B', 129) if fin else struct.pack('B', 0)
        msg_len = len(msg)
        if msg_len <= 125:
            data += struct.pack('B', msg_len)
        elif msg_len <= (2**16 - 1):
            data += struct.pack('!BH', 126, msg_len)
        elif msg_len <= (2**64 - 1):
            data += struct.pack('!BQ', 127, msg_len)
        else:
            # 分片传输超大内容（应该用不到）
            while True:
                fragment = msg[:(2**64 - 1)]
                msg -= fragment
                if msg > (2**64 - 1):
                   self.s.send(fragment, False)
                else:
                    self.s.send(fragment)
        data += bytes(msg)

        print (data)
        self.s.send(data)
        
    def recvexactly(self, sz):
        res = b""
        while sz:
            data = self.s.recv(sz)
            if not data:
                break
            res += data
            sz -= len(data)
        return res
    def read(self):
        while True:
            hdr = self.recvexactly(2)
            assert len(hdr) == 2
            firstbyte, secondbyte = struct.unpack(">BB", hdr)
            mskenable =  True if secondbyte & 0x80 else False
            length = secondbyte & 0x7f
            if DEBUG:
                print('test length=%d' % length)
                print('mskenable=' + str(mskenable))
            if length == 126:
                hdr = self.recvexactly(2)
                assert len(hdr) == 2
                (length,) = struct.unpack(">H", hdr)
            if length == 127:
                hdr = self.recvexactly(8)
                assert len(hdr) == 8
                (length,) = struct.unpack(">Q", hdr)
            if DEBUG:
                print('length=%d' % length)
            opcode =  firstbyte & 0x0f
            if opcode == 8:
                self.s.close()
                return ''
            fin = True if firstbyte&0x80 else False
            if DEBUG:
                print('fin='+str(fin))
                print('opcode=%d'%opcode)
            if mskenable:
                hdr = self.recvexactly(4)
                assert len(hdr) == 4
                (msk1,msk2,msk3,msk4) = struct.unpack(">BBBB", hdr)
                msk = [msk1,msk2,msk3,msk4]
            #print('msk'+str(msk))
            # debugmsg("Got unexpected websocket record of type %x, skipping it" % fl)
            data = []
            while length:
                skip = self.s.recv(length)
                # debugmsg("Skip data: %s" % skip)
                length -= len(skip)
                data.extend(skip)
            newdata = []
            #解码数据
            for i,item in enumerate(data):
                j = i % 4
                newdata.append(chr(data[i] ^ msk[j]))
            res = ''.join(newdata)
            return res
            
    def server_handshake(self):
        clr = self.s.makefile("rwb", 0)
        l = clr.readline()
        #sys.stdout.write(repr(l))
        webkey = None
        while 1:
            l = clr.readline()
            if not l:
                raise OSError("EOF in headers")
            if l == b"\r\n":
                break
        #    sys.stdout.write(l)
            h, v = [x.strip() for x in l.split(b":", 1)]
            if DEBUG:
                print((h, v))
            if h == b'Sec-WebSocket-Key':
                webkey = v

        if not webkey:
            raise OSError("Not a websocket request")

        if DEBUG:
            print("Sec-WebSocket-Key:", webkey, len(webkey))

        respkey = webkey + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        respkey = hashlib.sha1(respkey).digest()
        respkey = binascii.b2a_base64(respkey)[:-1]

        resp = b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % respkey

        if DEBUG:
            print(resp)
        self.s.send(resp)
        
    def client_handshake(self):
        cl = self.s.makefile("rwb", 0)
        cl.write(b'GET / HTTP/1.1\r\nHost: echo.websocket.org\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Key: foo\r\n\r\n')
        l = cl.readline()
    #    print(l)
        while 1:
            l = cl.readline()
            if l == b"\r\n":
                break
    #        sys.stdout.write(l)  

        
if __name__ == "__main__":
  sock = socket.socket()
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  ip=network.WLAN(network.STA_IF).ifconfig()[0]
  sock.bind((ip, 88))
  sock.listen(5)
  print('websokcet listen at %s:%s'%(ip,88))
  while True:
      # 这里阻塞接收客户端
      conn, address = sock.accept()
      # 接收到socket
      print('client connect...:')
      #初始化对象
      ws=websocket(conn)
      #开始握手
      ws.server_handshake()
      print('websocket connect succ')
      while True:
          #ws.write("hello") #发送二进制
          #ws.send("hello") #发送文本
          text = ws.read()
          if text =='':
              break
          print(text)  
