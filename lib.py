





















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
def ap(ssd,pwd='',active=1):
    
    ap= network.WLAN(network.AP_IF)
    ap.active(active)
    try:
      if pwd=='':
        ap.config(essid=ssd, authmode=network.AUTH_OPEN)
        return "success!"
      else:
        ap.config(essid=ssd, authmode=network.AUTH_WPA_WPA2_PSK, password=pwd)
        return "success!"
    except Exception as e:
      return str(e)
def pwm(pin,f,d,):
  pwm2 = PWM(Pin(pin), freq=f, duty=d)
#呼吸灯 gpio 需要空的脚管 MAX 最大亮度等级 step 呼吸灯步长,越小越流畅 lev 亮度初始值
def Breathe(gpio=2,max=1000,step=10,lev=1):
 
    while True:
        lev+=step
        i=lev
        if lev>max:
            i=max*2-lev
            if i<0:
                break
        time.sleep(0.01)
        #print (i)
        pwm2 = PWM(Pin(gpio), freq=100, duty=i)


    ##print (12)


def bb(p,f=1000,d=250,t=0.5):
  '''
  蜂鸣器
  p: gpio ,w周期，m：脉宽



  '''


  pwm22 = PWM(Pin(p), freq=f, duty=d)
  time.sleep(t)
  pwm22.deinit()

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


#gpio 控制的引脚
#st 引脚的值
pin_s={}
def pin(gpio=2,st=1):
    global pin_s
    if st==1:
        Pin(gpio,Pin.OUT).value(1)
        pin_s[gpio]=1
    elif st==0:
        Pin(gpio,Pin.OUT).value(0)
        pin_s[gpio]=0
    elif st==2:
        try: 
          return pin_s[gpio]
        except:
          pin_s[gpio]=0
          return 1
       




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

##WiFi链接模块    
def wifi(ssd='',pwd='',hostname="micropython"):
      wifi0 = network.WLAN(network.STA_IF)  #创建连接对象 如果让ESP32接入WIFI的话使用STA_IF模式,若以ESP32为热点,则使用AP模式   
      if ssd=='':
        return wifi0
      wifi0.active(True) #激活WIFI
      # 启用mdns
      wifi0.config(dhcp_hostname=hostname,mac=wifi0.config('mac'))
      wifi0.disconnect()
      print('connecting to network[正在连接]...')
      wifi0.connect(ssd, pwd) #essid为WIFI名称,password为WIFI密码
      for i in range(0,10):
              time.sleep(1)
              if wifi0.isconnected():
                print (wifi0.ifconfig())
                return True
      return False


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


