



from time import sleep_ms
from machine import Pin

pin=[16,5,4,0]#对应IN1到 IN4的GPIO引脚
Pin_All=[Pin(p,Pin.OUT) for p in pin]# 不要用GPIO1 否则模块会卡死-_- 找了半天才找到原因
#转速(ms) 数值越大转速越慢 最小值1.8ms








speed=2


STEPER_ROUND=512 #转动一圈(360度)的周期








ANGLE_PER_ROUND=STEPER_ROUND/360 #转动1度的周期




#print('ANGLE_PER_ROUND:',ANGLE_PER_ROUND)

def SteperWriteData(data):


    count=0


    for i in data:
        Pin_All[count].value(i)
        count+=1
        

def SteperFrontTurn():
    global speed
     
    SteperWriteData([1,1,0,0])
    sleep_ms(speed)

    SteperWriteData([0,1,1,0])
    sleep_ms(speed)

    SteperWriteData([0,0,1,1])
    sleep_ms(speed)
     
    SteperWriteData([1,0,0,1])   
    sleep_ms(speed)
     
def SteperBackTurn():
    global speed
     
    SteperWriteData([1,1,0,0])
    sleep_ms(speed)
     
    SteperWriteData([1,0,0,1])   
    sleep_ms(speed)
     
    SteperWriteData([0,0,1,1])
    sleep_ms(speed)

    SteperWriteData([0,1,1,0])
    sleep_ms(speed)


def SteperStop():
    SteperWriteData([0,0,0,0])
     
def SteperRun(angle):
    global ANGLE_PER_ROUND
     
    val=ANGLE_PER_ROUND*abs(angle)
    if(angle>0):
        for i in range(0,val):
            SteperFrontTurn()
    else:
        for i in range(0,val):

            SteperBackTurn()
    angle = 0
    SteperStop()
    
    





