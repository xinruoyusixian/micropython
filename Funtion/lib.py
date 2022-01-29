


import network
from machine import Pin, PWM ,RTC,Timer
import time,machine,ntptime,sys
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



def update_time():

      ntptime.host='ntp1.aliyun.com'
      try:
        ntptime.settime()
      except:
        print("TIME UPGRADE FAILED")
        return
      list=time.localtime(time.time()+8*60*60)
      rtc = RTC()
      rtc.datetime((list[0], list[1], list[2] ,None,list[3], list[4], list[5] ,0)) 
      print (rtc.datetime())

def wifi(ssd='',pwd='',hostname="MicroPython"):
      wifi0 = network.WLAN(network.STA_IF)
      wifi0.active(1)  
      if ssd=='':
        return (wifi0,'')
      wifi0.active(True) #激活WIFI
      # 启用mdns
      wifi0.config(dhcp_hostname=hostname,mac=wifi0.config('mac'))
      wifi0.disconnect()
      _s_time=time.time()
      if not wifi0.isconnected(): #判断WIFI连接状态
          print('[WIFI]:Connect to',ssd)
          wifi0.connect(ssd, pwd) #essid为WIFI名称,password为WIFI密码
          while (wifi0.ifconfig()[0]=="0.0.0.0"):
            time.sleep(1)
            if (time.time()- _s_time)>60:#60秒后失败
              print('[WIFI]:Connect Faied')
              return (wifi0,False)
    
      print('[WIFI]:', wifi0.ifconfig())
      return (wifi0,True)

class btn:
  
  def __init__(self,p):
    self.time_ms=time.ticks_ms
    self._btn=Pin(p,Pin.IN)
    self._btn.irq(handler=self.FALLING,trigger=(Pin.IRQ_FALLING))
    self.tim=Timer(-999)
    self.pressTime=500
    self.clickTimeMin=80#单机最小时间
    self.timeRising=0
    self.cb_press=None
    self.cb_click=None
    self.cb_click2=None
    self.diffTime1=999
    self.timeArr=[0,0]

  def FALLING(self,_e=0):
      self.timeFalling=self.time_ms()
      self.timeArr.append(self.timeFalling)
      self.timeRising=0
      self.tim.init(period=1, mode=Timer.PERIODIC, callback=self.check) 
      self._btn.irq(handler=self.RISING,trigger=(Pin.IRQ_RISING))
      
  def clickDely(self,_e=0):
    self.diffTime1=self.time_ms()-self.clickRuntime
    if self.diffTime1>300:
      self.tim1.deinit()
      print("click")
      self.cb(self.cb_click)
      
  def RISING(self,_e=0):
      self.timeRising=self.time_ms()
      self.tim.deinit()
      self._btn.irq(handler=self.FALLING,trigger=(Pin.IRQ_FALLING))
      diffTime=self.timeRising-self.timeFalling
      if diffTime > self.clickTimeMin and diffTime <self.pressTime :
          #click event delay, if you don't want to use doubleClick you can delete it,put click code at here
          if self.diffTime1<300 and (self.time_ms()-self.timeArr[-2])<500:
            self.tim1.deinit()
            print("doubleClick")
            self.cb(self.cb_click2)
            return
          self.clickRuntime=self.time_ms()
          self.tim1=Timer(-998)
          self.tim1.init(period=1, mode=Timer.PERIODIC, callback=self.clickDely) 

  def press(self,cb,s=0):
      self.cb_press=cb
      self.pressTime= self.pressTime if s==0 else s
      
  def click(self,cb):
      self.cb_click=cb
      
  def cb(self,cb):
        if cb.__class__.__name__ != 'NoneType':
           cb()  
  def doubleClick(self,cb):
      self.cb_click2=cb
  def check(self,_e=0):
      diffTime=self.time_ms()-self.timeFalling
      if diffTime >= self.pressTime:
        print("press",diffTime)
        self.tim.deinit()
        self.cb(self.cb_press)



