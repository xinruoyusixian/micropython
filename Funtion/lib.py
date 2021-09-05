






















#PWM 工作模板#
#pwm0 = PWM(Pin(0))      # 通过Pin对象来创建PWM对象
#pwm0.freq()             # 获得当前的PWM频率
#pwm0.freq(1000)         # 设置PWM频率
#pwm0.duty()             # 获得当前的PWM占空比
#pwm0.duty(200)          # 设置占空比
#PWM 简写
#pwm2 = PWM(Pin(2), freq=200, duty=1099)# 创建PWM同时设置参数
#pwm0.deinit()           # 关闭PWM
#上传温度
import  urequests
import network
from machine import Pin, PWM ,RTC
import time,dht,machine,ujson,ntptime,sys

def ap(ssd,pwd=''):
    AP= network.WLAN(network.AP_IF)
    if ssd=='':
      AP.active(0)
      return (AP,True)
    try:
      AP.active(1)
      AP.config(essid=ssd, authmode=network.AUTH_WPA_WPA2_PSK, password=pwd) if pwd != '' else AP.config(essid=ssd, authmode=network.AUTH_OPEN)
      return (AP,True)
    except Exception as e:
      print (e)
      return (AP,False)
      
def file(file,c=''):
    if c=='':
      try:
        f=open(file,"r")
        return f.read()
      except Exception as e:
        print(e,"文件不存在")
        return False
    else:
      f=open(file,"w")
      f.write(c)
      f.flush()
      f.close()
      
class flashLed:
    def __init__(self,pin):
      self.pin=Pin(pin,Pin.OUT)
      self.delay=250
      self._time1=time.ticks_ms()
      self.period=1
      self.freq=100
      self.max=1022
      self.duty=self.max      
    def sw(self,s=2,delay=250):
      if type(s).__name__=="Timer" or s==2:
        if (time.ticks_ms()- self._time1)>self.delay:
          self.delay= self.delay if delay==250  else delay
          self.pin.value(0) if self.pin.value() else self.pin.value(1)
          self._time1=time.ticks_ms()
      if s==1:
        self.pin.value(1)
        return
      if s==0:
        self.pin.value(0)
        return
      if s=="":
        return self.pin.value()        
      
    def flash(self,delay=250):
        self.delay=delay
        self.timer(self.sw)
        return
    def stop(self):
        try:
          self.tim.deinit()
          del self.tim
        except:
          pass
        try:
          time.sleep_ms(50)
          self.pwm.deinit()
        except:
          pass 
        self.pin.init(Pin.OUT)

        return
    def timer(self,cb):
        self.tim=Timer(-1)  
        self.tim.init(period=self.period, mode=Timer.PERIODIC, callback=cb)
    def bre(self,loop=1,step=1):
        self.step=step
        if loop==1:
          self.stop()
          self.timer(self.repat)
        if loop==0:
          self.repat()
        return  
    def repat(self,s=1):
        self.pwm = PWM(self.pin)
        self.duty=self.duty-self.step
        if self.duty< -self.max:
           self.duty=self.max
        self.pwm.init(freq=self.freq, duty=abs(self.duty))
        return


#测温度
def dhts(pin,dh=11):
  if dh==11:
    d=dht.DHT11(machine.Pin(pin))
  if dh==22:
    d=dht.DHT22(machine.Pin(pin))
  a=[]
  try:
      time.sleep(1)
      d.measure() 
      #print ("---------------------")
      #print ("温度", d.temperature() )
      #print ("湿度" ,d.humidity())
      a=[d.temperature(),d.humidity()]
    #except OSError as e:
  except Exception as e:
       #print ("出错")
       a=['err','err']
       pass
  return a


def update_time_http():
    URL="http://quan.suning.com/getSysTime.do"
    try:
      res=urequests.get(URL).text
      j=ujson.loads(res)
      list=j['sysTime1']
      rtc = RTC()
      #rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
      rtc.datetime((int(list[0:4]), int(list[4:6]), int(list[6:8]) ,8,int(list[8:10]), int(list[10:12]), int(list[12:14] ),0)) 
      print (rtc.datetime()) # get date and time
    except OSError as e:
      print ("upgrde failed!")

def update_time():
      ntptime.host='ntp1.aliyun.com'
      try:
        ntptime.settime()
      except:
        print("TIME UPGRADE FAILED")
        return
      list=time.localtime(time.time()+8*60*60)
      rtc = RTC()
      #rtc.datetime((year, month, mday, 0, hour, minute, second, 0))
      rtc.datetime((list[0], list[1], list[2] ,None,list[3], list[4], list[5] ,0)) 
      print (rtc.datetime()) # get date and time


      


#网络检测 
def  isOline():
  try:
   html = urequests.get("http://www.baidu.com")
  except:
   return False
  return True

class  _wifi:
 
  def __init__(self,ssd,pwd):
    self.ssd=ssd
    self.pwd=pwd
    self.hostname="micropython" 
    self.wifi0 = network.WLAN(network.STA_IF)  
  def connect(self):
    self.wifi0.active(True) #激活WIFI
    self.wifi0.config(dhcp_hostname=self.hostname)
    if not self.wifi0.isconnected(): #判断WIFI连接状态

          print('[wifi]:正在连接...')

          self.wifi0.connect(self.ssd, self.pwd) #essid为WIFI名称,password为WIFI密码

          while not self.wifi0.isconnected():

              pass # WIFI没有连接上的话做点什么,这里默认pass啥也不做

    print('network config[网络信息]:', self.wifi0.ifconfig())    

  def mdns(self,host=0):
    self.disconnect()
    self.hostname=host
    print(host,".local")
    time.sleep(1)
    self.connect()
  def disconnect(self):
    self.wifi0.disconnect()
    
  def info(self):
    return self.wifi0.ifconfig()

