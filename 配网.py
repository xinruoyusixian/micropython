


import socket,re,network
from machine import Pin,lightsleep,reset,Timer

def wifi_web():
  wifi_conf="wifi_conf.py"
  def getargs(s):
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
  tim = Timer(-1)
  tim.init(period=100, mode=Timer.PERIODIC, callback=lambda t:exec('_led=Pin(2, Pin.OUT);_led( not _led.value()); ')) #周 期  
  ap= network.WLAN(network.AP_IF)
  sta=network.WLAN(network.STA_IF)
  ap.active(1)
  ap.config(essid="ESP8266", authmode=network.AUTH_OPEN)
  ip =ap.ifconfig()[0]
  port = 80
  webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建套接字
  webserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #设置给定套接字选项的值
  webserver.settimeout(2000)
  webserver.bind((ip, port))                                       #绑定IP地址和端口号
  webserver.listen(5)                                              #监听套接字
  print("服务器地址:%s:%d" %(ip,port))
  while True:
    conn, addr = webserver.accept()                                #接受一个连接，conn是一个新的socket对象
    request = conn.recv(1024)                             #从套接字接收1024字节的数据
    if len(request)>0:
      request = request.decode()
      result = re.search("(.*?) (.*?) HTTP/1.1", request)
      if result:
        #method = result.group(1)
        url = result.group(2)
        #conn.sendall("HTTP/1.1 200 OK\nConnection: close\nServer: Esp8266\nContent-Type: text/html;charset=UTF-8\n\n")
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send("Server: Esp8266\r\n")
        conn.send("Content-Type: text/html;charset=UTF-8\r\n")
        conn.send("Connection: close\r\n")
        conn.send("\r\n")
        if url =="/":
          ap_list=sta.scan()
          conn.sendall('<form action="wifi">SSD:<br><input type="text" name="ssd" value=""><br>PASSWORD<br><input type="text" name="pwd" value=""><br<br><input type="submit" value="Submit"></form> ')
          conn.sendall('<hr/>')
          for i in ap_list:
            conn.sendall("%s ,%d<br/>"%(i[0].decode(),i[3]))
          #conn.sendall(html)
        if url.find("/wifi")!=-1:
            d=(getargs(url))
            print(d)
            if d.get("ssd") !=None and d.get("pwd")!=None:
              print("connecting")
              sta.active(True)
              sta.connect(d.get("ssd"), d.get("pwd"))
            for i in range(0,10):
              lightsleep(1000)
              if sta.isconnected():
                  conn.sendall("CONNECTED!<hr/> wating Restart")
                  conn.send("\r\n")
                  lightsleep(1000)
                  ap.active(0)
                  w_str='{"ssd":"%s","pwd":"%s"}'%(d.get("ssd"),d.get("pwd"))
                  fo = open(wifi_conf, "w")
                  fo.write(w_str)
                  fo.close()  
                  reset()
            conn.sendall("CONNECT FAILED<br/><button onclick='window.history.back()'>Back</button>")  
        conn.send("\r\n")  # 发送结束
      else:
        print("not found url")
        
    else:
      print("no request")
    conn.close()







