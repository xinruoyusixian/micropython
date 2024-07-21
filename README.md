# micropython
micropython 显示中文
micropython 显示汉字
esp8266 esp32 显示汉字

ssd1306.py 这个是新修改的 可以显示字符画或者中文.测了一个用oled.py能画的字符画 这个内存不足.
oled.py    这个也是ssd1306的驱动  不过是直接操作显存 不用framebuffer 很省内存.

 oled 0.91寸 初始化 
        cmd=[
          [0xae],		     #display off
          [0xa6],         #Set Normal Display (default)

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
          [0x02],         #0x12#128x32 OLED: 0x002,  128x32 OLED 0x012
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
