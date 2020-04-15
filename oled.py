
class oled:
    def __init__(self,i2c):
        self.i2c = i2c
        self.ADDR = 0x3C
        cmd = [
        [0xAE],                    # DISPLAYOFF
        [0xA4],           #显示恢复
        [0xD5, 0xF0],            # 设置显示时钟SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],                  # 设置多重 SETMULTIPLEX
        [0xD3, 0x00],              # 设置显示偏移SETDISPLAYOFFSET
        [0 | 0x0],                   # 设定起始行 SETSTARTLINE
        [0x8D,  0x14],                    # CHARGEPUMP
        [0x20,  0x00],  #  内存模式水平 MEMORYMODE horizontal
        [0x21,  0, 127],  # 列地址 COLUMNADDR
        [0x22,  0, 63],   # 页面地址 PAGEADDR
        [0xa0 | 0x1],  # SEGREMAP
        [0xc8],   #  通讯扫描COMSCANDEC
        [0xDA,  0x12],                    #设置组合 SETCOMPINS
        [0x81,  0xCF],                   #  SETCONTRAST
        [0xd9,  0xF1],                  # SETPRECHARGE
        [0xDB,  0x40],                 # SETVCOMDETECT
        [0xA6],                 # NORMALDISPLAY
        [0xd6, 0],  # zoom off
        ]
        for c in cmd:
            self.command(c)
        self.clear()
        self.command([0xaf])  # SSD1306_DISPLAYON
    def set(self,rect):
      #设置范围 rect[0],rect[1] 从列到几列最大127
      #         rect[2],rect[3] 从行到几行最大7
        self.command([0x21, rect[0], rect[1]]) 
        self.command([0x22, rect[2], rect[3]])
    def clear(self,rect=[0, 127, 0, 7]):
        self.set(rect)
        screen = bytearray(33)
        screen[0] = 0x40
        for i in range(0, 32):
            self.write(screen)
            
    def command(self,c):
        self.i2c.writeto(self.ADDR, b'\x00' + bytearray(c))
        
    def write(self,b):
      self.i2c.writeto(self.ADDR, b)
      # 一个十六进制 控制每一列向下的8个像素
      #i2c.writeto(ADDR, b'@0\x00\x00\x00\x000')
        


    def draw(self,arr,x,y):


        self.set([x,127,y,7])
        print(x,y)
        for i in range(0,len(arr)):
            self.write(arr[i])
            y+=1 
            self.set([x,127,y,7])
            print(x,y)
    def  fill(self,s,b=1000):
        p=0  
        while 1:
          self.write(s)
          p+=1
          if p==b:
            break
         
                     
       
           
if __name__ == "__main__":
  from machine import Pin, I2C
  i2c=I2C(scl=Pin(4), sda=Pin(5))
  import time,font
  from time import sleep
  num=font.num
  ch=font.ch
  font=font.font
  d=oled(i2c)
  draw=d.draw
  clear=d.clear
  def display(s):
      
      s=str(s)

      x=0
      draw(font[int(s[0:1])],x,0)
      x+=20
      draw(font[int(s[1:2])],x,0)
      x+=20
      draw(font[10],x,0)
      x+=2
      draw(font[int(s[2:3])],x,0)
      x+=20
      draw(font[int(s[3:4])],x,0)
      x+=20
      draw(font[10],x,0)
      x+=2
      draw(font[int(s[4:5])],x,0)

      x+=20
      draw(font[int(s[5:6])],x,0)
  while 1:
    
    th=lib.dhts(14,22)
    t=str(th[0])
    h=str(th[1])    
    
    clear()
    draw(ch[0],1,1)
    draw(ch[2],25,1)
    draw(num[11],51,1)
    draw(ch[1],1,4)
    draw(ch[2],25,4) 
    draw(num[11],51,4)
  

    draw(num[int(t[0])],65,1)
    draw(num[int(t[1])],78,1)
    draw(num[10],90,1)
    draw(num[int(t[3])],95,1)
    draw(ch[3],105,1)
    
    draw(num[int(h[0])],65,4)
    draw(num[int(h[1])],78,4)
    draw(num[10],90,4)
    draw(num[int(h[3])],95,4)
    draw(num[12],110,4)
    
    sleep(1)
    t=time.localtime()

    t=str("%02d" % t[3])+str("%02d" % t[4])+str("%02d" % t[5])
    clear()
    display(t)
    
    sleep(1)
