
import machine,re,gc,os,ujson,utime,blinker,lib
from machine import Pin,UART,Timer
from utime import sleep 
import utime as time 
import web配网,lib,time,ujson

try:
    with open('wifi_conf.py', 'r+') as f:
      json_data = ujson.load(f)
      if not lib.wifi(json_data['ssd'],json_data['pwd']):
        print ("连接失败！")
        raise "连接失败！"

except Exception as e:
          web.wifi_web()





lib.pin(2,0)
def send(s):
    uart = UART(1, 38400)                 # init with given baudrate
    uart.init(38400, bits=8, parity=None, stop=1) 
    print("send:",s)
    uart.write(s) 
def publish(msg):
      mq.publish(msg)
      
def time_add(t,add):
    #t=[10,11,12] #时间加秒
    _tmp=divmod(t[2]+add,60)
    t[2]=_tmp[1]
    if _tmp[0]>0:
        t[1]+=_tmp[0]
    if t[1]>=60:
        _tmp=divmod(t[1],60)
        t[1]=_tmp[1]
        t[0]+=_tmp[0]
    return t

def pin_sw(p):
      try:
        lib.pin_s[p]
      except:
        lib.pin_s[p]=0
      if lib.pin_s[p]==1:
        lib.pin(p,0)
      else:
        lib.pin(p,1)  
def cb(topic, msg):
        print("Mqtt REC<<<<",topic,msg)
        msg=eval(str(msg)[2:-1]) 
        try:
            if(msg['data']['get']=='state'):
              mq.onLine()
              return
              
        except:
          pass
        
        try:
          if str(msg['data']).find("btn")>-1:
              index=list(msg['data'].keys())[0]
              print(index)
              if index[4:]=='sw': 
                  pin_sw(12)
                  return
              if msg['data'][index]=='tap':
                  print("tap:",index)
                  send(index[4:])
                  
          if str(msg['data']).find("ran-vol")>-1:
                send("AT+VOL="+str("%02d" % msg['data']['ran-vol']))  
                return 
          if str(msg['data']).find("ran-timeout")>-1:
                tim_sec=60*int(msg['data']['ran-timeout'])
                t=time.localtime()
                t=[t[3],t[4],t[5]]
                t=time_add(t,tim_sec)
                tim.timer(t)
                mq.publish("Timeout: %s"%str(t))
                return
        except:
          print("something")
          return

          


#tim=Timer(-1)
#tim.init(period=3000,mode=Timer.PERIODIC, callback=lambda t:print(0))

class timer:
  def __init__(self,t=500):
      self.tim=Timer(-1)
      self.t=t
      self.mode=self.tim.PERIODIC
  def timer(self,time):
    self.time=time
    self.tim.deinit()
    self.tim.init(period=self.t,mode=self.mode,callback=self._time_diff)

  def _time_diff(self, args):
    t=time.localtime()
    t=[t[3],t[4],t[5]]
    if t==self.time:
      lib.pin(12,0)

  
send("AT")
tim=timer()

lib.update_time()
blinker.DEBUG=1
mq=blinker.blinker("6cf52fc82da2",cb)
mq.connect()
while 1:
    time.sleep_ms(100)
    t=time.localtime()
    if t[5]==0:
      mq.ping()
      time.sleep(1)
    try:
      mq.check_msg()
    except:
      pass









