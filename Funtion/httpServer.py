import socket,re,network,os


class http:
  def __init__(self,ip,port):
    self.IP=ip
    self.PORT=port
    self.webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建套接字
    self.webserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #设置给定套接字选项的值
    self.webserver.settimeout(2000)
    self.webserver.bind((ip, port))                                       #绑定IP地址和端口号
    self.webserver.listen(5)                                              #监听套接字
    self.header="HTTP/1.1 200 OK\r\nServer: Esp8266\r\nContent-Type: text/html;charset=UTF-8\r\n"
    print("服务器地址:%s:%d" %(ip,port))
    
    
  def http(self,cb):    
      self.conn, self.addr = self.webserver.accept()
      request = self.conn.recv(1024) 

      if len(request)>0:

        request = request.decode()

        result = re.search("(.*?) (.*?) HTTP/1.1", request)
        if result:
          method = result.group(1)
          url = result.group(2)
          print("URL:",url,"Method:",method) 
          self.sendall(self.header)
          self.conn.send("Connection: close\r\n")
          self.conn.send("\r\n")
          try:
            cb(url)
          except  Exception as e:
            self.sendall(str(e))
        self.send("\r\n")
        self.conn.close() 
        print("out %s" % str(self.IP))     
  def send(self,s):
    self.conn.send(s)
  def sendall(self,s):
    self.conn.sendall(s)    
  def get_Args(self,s):
      q=s.find("?")
      if q ==-1 or s.find("=")==-1:
        return  False
      s=s[q+1:]
      args=s.split("&")
      data={}
      for i in args:
        tmp=i.split("=")
        data[tmp[0]]=tmp[1]
      return data
      

