## IR MODE
from machine import UART
import   time
class IR:
 
  def __init__(self,rx,tx):
    self.uart = UART(1, baudrate=115200, rx=rx,tx=tx,timeout=10)
    self._write_flag=0
    self.ac_state=0
    
  def uartSend(self,t):
    self.uart.write(t)
    
  def write(self,name,str):
    f=open(name,"wb")
    f.write(str)
    f.close()
    
  def read(self,name):
    f=open(name,"rb")
    data=f.read()
    f.close()
    return data

  def main(self):
      time.sleep_ms(100)
      if self.uart.any():
          a=self.uart.read()
          if a!=b'\xfe\xfc\xcf':
            if self._write_flag:
              file_name="ir_Data/Ac_"+ self._write_flag
              self.write(file_name,a)
          return a
 

