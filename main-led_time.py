

import   time ,lib,blinker,font,oled
from machine import Pin, I2C
i2c=I2C(scl=Pin(5), sda=Pin(4))
d=oled.oled(i2c)
font=font.font
draw=d.draw
clear=d.clear  

def display(init=False):
    _t=time.localtime()
    s=str("%02d" % _t[3])+str("%02d" % _t[4])+str("%02d" % _t[5])
    y=1
    clear([105,105+20,y,50])
    draw(font[int(s[5])],105,y)
    if s[5]=="0" or init  :
        clear([85,85+20,y,y+50])
        draw(font[int(s[4])],85,y)
    if s[4:6]=="59" or init  :
            clear([83,83+2,y,y+50])
            draw(font[10],83,y)          
            clear([43,43+20,y,y+50])
            draw(font[int(s[2])],43,y)

            clear([63,63+20,y,y+50])
            draw(font[int(s[3])],63,y)
            clear([41,41+2,y,y+50])
            draw(font[10],41,y)
            clear([1,1+20,y,y+50])
            draw(font[int(s[0])],1,y)
            clear([21,21+20,y,y+50])
            draw(font[int(s[1])],21,y)
            
def cb(topic, msg):
        global led_sw,interval,survial,tmp
        print("Mqtt REC<<<<",msg)
        #传感器操作
        msg=eval(str(msg)[2:-1])
        print("Mqtt接收<<<<",msg)
        #电灯操作
        try:
          if msg['data']['btn-sw']=='tap':
             timer=0
             if lib.pin_s[12]==0:
               lib.pin(12,1)
               mq.publish({"btn-sw":{"tex":"ON"}})    
             else:
              lib.pin(12,0)
              interval=0
              survial=0
              mq.publish({"btn-sw":{"tex":"OFF"}})    
        except:
          pass 
        try:
          
          if msg['data']['btn-led-sw']=='tap':
             if led_sw==0:
                led_sw=1
                mq.publish({"btn-led-sw":{"swi":"on","col":"#00FF00"}})    
             else:
                led_sw=0
                
                mq.publish({"btn-led-sw":{"swi":"off"}})  
        except:
          pass 
        try:
            if str(msg['data']).find("interval")>-1:
              interval=msg['data']['interval']+survial
              tmp=0
        except:
          pass
        try:
            if str(msg['data']).find("survial")>-1:
              survial=msg['data']['survial']
              
        except:
          pass          
        if msg['fromDevice']=='MIOT':
          try:
            if(msg['data']['set']['pState']=='true'):
              print("on")
              lib.pin(12,1)
              
            else:
              print("off")
              lib.pin(12,0)
              interval=0
              survial=0
              
          except:
            pass 
        
        mq.publish("%s"% lib.wifi("","","info")[0])   
        print("exec")

a="0"
mq=blinker.blinker("b14b891ec11b",cb,'light')

  
def pin_sw(p):
      if lib.pin_s[p]==1:
        lib.pin(p,0)
      else:
        lib.pin(p,1)  

t=1
lib.pin(2,1)
lib.update_time()
lib.pin(12,0)
mq.ping()
display(1)
led_sw=1
survial=0 
interval=0
tmp=0
while 1:
      time.sleep(1)
      try:
        display()
      except:
        print("oled err")
      if t%10000==0:
        lib.update_time()
      if t%61==0:
        mq.ping()
      if led_sw==1:
        pin_sw(2)
      
      if interval and survial:
          if tmp==0:
              lib.pin(12,1)
          if tmp==survial:
              pin_sw(12)
          tmp+=1      
          if tmp==interval:
              tmp=0
          
      t+=1
      mq.check_msg()

























