




import framebuf
class oled:
    def __init__(self,i2c,height=64,width=128):
        self.buffer =  bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        self.i2c = i2c
        self.ADDR = 0x3C
        cmd64= [
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
        cmd32=[
          [0xAE],        	# DISPLAYOFF
          [0xD5],        	# SETDISPLAYCLOCKDIV
          [0x80],        	# the suggested ratio 0x80
          [0xA8],        	# SSD1306_SETMULTIPLEX
          [0x1F],
          [0xD3],        	# SETDISPLAYOFFSET
          [0x00],         	# no offset
          [0x40 | 0x0],  	# SETSTARTLINE
          [0x8D],        	# CHARGEPUMP
          [0x14],         #0x014 enable, 0x010 disable

          [0x20],         #com pin HW config, sequential com pin config (bit 4), disable left/right remap (bit 5),
          [0x00],         #128x64:0x00     128x32 : 0x02, or 128x32 OLED 0x12  
          [0xa1],         #segment remap a0/a1
          [0xc8],         #c0: scan dir normal, c8: reverse
          [0xda],
          [0x02],         #com pin HW config, sequential com pin config (bit 4), disable left/right remap (bit 5)
          [0x81],
          [0xcf],         #[2] set contrast control
          [0xd9],
          [0xf1],         #[2] pre-charge period 0x022/f1
          [0xdb],
          [0x40],         #vcomh deselect level

          [0x2e],         #Disable scroll
          [0xa4],         #output ram to display
          [0xa6],         #none inverted normal display mode
          [0xaf]        #display on
            ]
        cmd= cmd32 if(height==32) else cmd64
        del cmd32
        del cmd64
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
        
    def fill(self,col):
        self.framebuf.fill(col)
        
    def pixel(self,x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self,string, x, y, col=1):
        self.framebuf.text(string, x, y, col)        
    def write(self,b):
      self.i2c.writeto(self.ADDR, b)
      # 一个十六进制 控制每一列向下的8个像素
      #i2c.writeto(ADDR, b'@0\x00\x00\x00\x000')


    





    def string(self,s):


      #在指定位置写入8*8的文字 会自动向后显示文字


      w=len(s)*8


      h=8


      buffer= bytearray(((h // 8) * w) + 1)


      buffer[0] = 0x40  


      fbuf = framebuf.FrameBuffer(memoryview(buffer)[1:], w, h, framebuf.MONO_VLSB)
      fbuf.text(s, 0, 0, 0xffff)
      print (buffer)
      self.write(buffer)        


    def draw(self,arr,x,y):
        self.set([x,127,y,7])
        for i in range(0,len(arr)):
            self.write(arr[i])
            y+=1 
            self.set([x,127,y,7])
    def  fill(self,s,b=1024):
        p=0  
        while 1:
          self.write(s)
          p+=1
          if p==b:
            break
         
                     
       
           
if __name__ == "__main__":
  from machine import Pin, I2C
  i2c=I2C(scl=Pin(14), sda=Pin(27))

  
  font=[
  [
  b"@\x00\x70\xFC\x06\xFA\xFF\xFF\x03\x03\xFF\xFF\xFE\x04\xFC\x70\x00",
  b"@\x00\x00\x01\x03\x06\x0F\xEF\xFC\xFC\xEF\x0F\x06\x03\x01\x00\x00",#气球16x16
  ],
  [

  b"@\x00\x1C\x7E\x7F\xE3\xC1\x81\x81\xC3\x7F\x7E\x1C",
  b"@\x00\x3C\x7E\x7F\xC3\x80\x81\x81\xC3\xFF\x7E\x3C",#8
  ],
  [
  b"@\x00\x80\x80\x04\x0C\x18\x18\x80\x00\xF8\xF8\xC8\xC8\xC8\xC8\xC8\xC8\xC8\xFC\xFC\x00\x00\x00\x00",
  b"@\x00\x00\x01\x07\x87\xF8\x7F\x07\xE0\xEF\x2F\x25\xE5\xE5\x25\xE5\xE5\x25\x2F\xEF\xE0\x20\x00\x00",


  b"@\x00\x01\x01\x3F\x3F\x3F\x20\x20\x3F\x3F\x20\x20\x3F\x3F\x20\x3F\x3F\x20\x20\x3F\x3F\x30\x30\x20",#温





  ],


  [#太阳


  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x0C\x0E\x1E\x7F\xFE\xF8\xF8\xF8\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81\x80\x80\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xF0\xF8\xF8\xFC\xFE\x7F\x1E\x0C\x00\x00\x00\x00\x00\x00\x00\x00",
  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x00\x80\xC0\xE0\xF0\xF8\xFC\x7E\x3E\x3F\x1F\x1F\x0F\x0F\x0F\x07\x07\x07\x0F\x0F\x0F\x1F\x1F\x3F\x3E\x7E\xFC\xF8\xE0\xE0\xC0\x00\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
  b"@\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\x00\x00\x00\x00\x00\x00\x00\xFE\xFF\xFF\xFF\x0F\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x1F\xFF\xFF\xFF\xFE\x00\x00\x00\x00\x00\x00\x00\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0",
  b"@\x03\x07\x07\x07\x07\x07\x07\x07\x03\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xF0\xC0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC0\xF8\xFF\xFF\xFF\x7F\x00\x00\x00\x00\x00\x00\x00\x03\x07\x07\x07\x07\x07\x07\x07",
  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x0F\x0F\x1F\x3F\x7E\x7C\xF8\xF8\xF8\xF0\xF0\xF0\xE0\xE0\xE0\xF0\xF0\xF0\xF8\xF8\xF8\x7C\x7E\x3F\x1F\x0F\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x20\x30\x78\xFE\x3F\x3F\x3F\x0F\x0E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x81\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0F\x1F\x3F\x3F\x7F\xFC\x78\x30\x00\x00\x00\x00\x00\x00\x00\x00",
  b"@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",#D:\ESB8266\资料\bmp\weather\qing.BMP#0#

  ]



  ]


  #默认是高度为64的oled  如果是32的d=oled(i2c,32)
  d=oled(i2c)





  #清屏 可带参数清除指定区域 [0,127,0,8]  (0,127) 宽度,(0,8)是高度  1个高度是8像素 


  d.clear()


  d.draw(font[3],0,0)


  d.draw(font[2],65,0)


  d.draw(font[0],65,3)



  d.draw(font[1],90,3)


  d.clear([65,127,5,7]) #清除此区域 在此区域输出
  d.string("12345-=%as")
