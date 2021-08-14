

from machine import Pin, I2C,UART,WDT,reset,SPI
from urequests import get
import   time ,lib,_thread,blinker,websocket,socket,machine,ujson,os



from IR_Model import IR
_ir= IR(33,32)
send=_ir.uartSend
read=_ir.read
def ir():
  
  while 1:
    d=_ir.main()
    if d!= None:
      print(d)
_thread.start_new_thread(ir, ())


class btn:
  def __init__(self,cb):
    self.debug=0
    #cb:需要触发的函数

    self.start=0
    self.cb=cb
    
  def click(self,_0=4):
    #按键消抖
    #_0:为无效参数，防止出错
    t=time.ticks_ms()-self.start
    if t<100:
      return
    if self.debug:
      print("Click",time.ticks_ms(),t)
    self.start=time.ticks_ms()
    self.cb()
    
    
 
 
class acTurn:
  
  
  def __init__(self):
    self.state=0
    self.list=os.listdir("/ir_data")

  
  def run(self):
    list_len=len(self.list)
    
    print(self.list[self.state])
    send(read("/ir_data/"+self.list[self.state]))
    if self.state>=(list_len-1):
      self.state=0
    self.state=self.state+1

  
  def off(self):
    if self.list[self.state]!='Ac_btn-off':
      self.state=self.list.index("Ac_btn-off")
      send(read("/ir_data/Ac_btn-off"))
    else:
      
      self.state=0
      send(read("/ir_data/"+self.list[self.state]))
      
  
  
ac=  acTurn()

#按键循环切换
_26=btn(ac.run)  
_26_btn=Pin(26,Pin.IN)
_26_btn.irq(handler=_26.click,trigger=(Pin.IRQ_FALLING))
#按键控制开关
_25=btn(ac.off)  
_25_btn=Pin(25,Pin.IN)
_25_btn.irq(handler=_25.click,trigger=(Pin.IRQ_FALLING))


wifi_name="wifi"
wifi_pwd="1234567788"
wlan=lib.wifi(wifi_name,wifi_pwd)
#netswitch
port=10086
ip = wlan.ifconfig()[0]
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  

s.bind((ip,port))

addr=('192.168.1.233', 10086)



def ws_send(msg):
    if ws.is_open:
         ws.send(str(msg))
         
def msg_send(msg):
         ws_send(msg)
         

def publish(msg):
      mq.publish(msg)
      ws_send(str(msg))

def hms(seconds):
#时间转换
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    #print ("%d:%02d:%02d" % (h, m, s))
    return (h, m, s)
    
def info():
          try:
            #传感器操作
            publish({"tex-02":{
                       "tex":"%s"%_ir.ac_state,
                       "tex1":"Conn:%s"%mq.connect_count},
                     "num-tmpr":{
                        "val":th[0]},
                        "num-humid":{"val":th[1]},
                      "tex-run":{
                        "tex":"%d:%d:%d" %hms(time.ticks_ms()/1000)}
            }) 
          except:
            print ("err")


def cb(topic, msg):
        try:
            
            if msg['deviceType']=='DiyArduino':
             
              index=msg['data']

              print("DIY:",index)
              if index[0]=='get':
                  mq.onLine()
                  info()
                  return
              if index[0].find("btn")>-1:
                  if index[0]=='btn-led':
                      return
                  if index[1]=='tap':
                    try:
                      file_name="ir_Data/Ac_"+ index[0]
                      send(read(file_name))
                      _ir.ac_state=index[0]
                    except:
                      publish("Command not exisit")
                    return 0  #结束运行
                  elif index[1]=='press':
                      print("press",index)
                      _ir._write_flag=index[0]
                  elif index[1]=='pressup':
                    print("up")
                    _ir._write_flag=0
        except:
          print("DiyArduino,出错。")
        try :
          if msg['deviceType']=="MIOT":
            mq.pubtopic_rrpc=topic[:47]+b'response'+topic[54:]  
            index=msg['data']
            print(index)
            if(index[0]=='get'):
                mq.publish({"pState":"True"},'mi')
                print("get")
            if index[0]=='set':
              if(index[1]['pState']=='true'):
                send(read("ir_Data/Ac_btn-28"))
                mq.publish({"pState":"True"},'mi')
                return
              if(index[1]['pState']=='false'):
                #send(read("ir_Data/Ac_btn-off"))
                mq.publish({"pState":"Flase"},'mi')
       
                return
        except:
          print("miot err")
webrepl.start()
time.sleep(2)
lib.update_time()

blinker.DEBUG=1
mq=blinker.blinker("fbc6da5da621",cb,'light')
mq.connect()
ws=websocket.websocket(81)
 
 
ms="" 

def ccb(msg):
       global ms
       time.sleep_ms(100)
       msg=eval(msg)
       msg={'data': [list(msg["data"].keys())[0], msg["data"][list(msg["data"].keys())[0]]], 'deviceType': 'DiyArduino'}
       print("websocket:",msg,"\n",type(msg))
       #print("websocket1:",msg)
       cb("websocket",msg   )

def web():
  global th
  while 1:
    time.sleep_ms(100)
    ws.msg_ckeck(ccb)

    
    



  
def mqtt():
  global th
  while 1:
    time.sleep_ms(100)
    _t=time.localtime()
    if _t[3]%5==0 and _t[5]==0:
          lib.update_time()

    if _t[5]==0:
        mq.ping()
        
        time.sleep(1)

    
    if not  wlan.isconnected():
      pass
    else:
      pass
    try:
      mq.check_msg()
    except:
      pass

 


_thread.start_new_thread(web, ())
_thread.start_new_thread(mqtt, ())



















































