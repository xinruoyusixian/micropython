#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import websocket_helper
import sys
import os
try:
    import ustruct as struct
except:
    import struct
    
DEBUG = False

class websocket:

    def __init__(self, s):
        self.s = s
        
    def write(self, data):
        l = len(data)
        if l < 126:
            # TODO: hardcoded "binary" type
            hdr = struct.pack(">BB", 0x82, l)
        else:
            hdr = struct.pack(">BBH", 0x82, 126, l)
        self.s.send(hdr)
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
            
            
if __name__ == "__main__":
  sock = socket.socket()
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind(("0.0.0.0", 8008))
  sock.listen(5)
  print('websokcet listen at 8008...')
  while True:
      # 这里阻塞接收客户端
      conn, address = sock.accept()
      # 接收到socket
      print('client connect...:')
      print(address)
      websocket_helper.server_handshake(conn)
      ws = websocket(conn)
      print('websocket connect succ')
      # conn.send('hello friend')
      while True:
          text = ws.read()
          if text =='':
              break
          print(text)  
