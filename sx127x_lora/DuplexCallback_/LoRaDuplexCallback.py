
import time,machine,ubinascii,sys

millisecond = time.ticks_ms
uuid = ubinascii.hexlify(machine.unique_id()).decode()  

msgCount = 0            # count of outgoing messages
INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
 


def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:] 
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:] 

def duplexCallback(lora):
    print("LoRa Duplex with callback")
    lora.onReceive(on_receive)  # register the receive callback
    do_loop(lora)


def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0
    NODE_NAME = 'ESP32_'  
    NODE_NAME = NODE_NAME + uuid
    while True:
        now = millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            message = "{} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)                              # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    # print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    lora.blink_led()   
            
    try:
        payload_string = payload.decode()
        rssi = lora.packetRssi()
        print("*** Received message ***\n{}".format(payload_string))
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(rssi))
    
