




from time import sleep
from machine import Pin, SPI, reset
            
class Controller:

    class Mock:
        pass        




    def __init__(self):
        # LoRa config
        self.PIN_ID_FOR_LORA_RESET = 25
        self.PIN_ID_FOR_LORA_SS = 26
        self.PIN_ID_SCK = 12
        self.PIN_ID_MOSI = 27
        self.PIN_ID_MISO = 14


        self.PIN_ID_FOR_LORA_DIO0 = 23
        #SCK,MISO,MOSI,SEL,RST | 12,14,27,26,25  #IO0|23

        self.PIN_ID_FOR_LORA_DIO1 = None 
        self.PIN_ID_FOR_LORA_DIO2 = None 
        self.PIN_ID_FOR_LORA_DIO3 = None
        self.PIN_ID_FOR_LORA_DIO4 = None
        self.PIN_ID_FOR_LORA_DIO5 = None
        self.pin_reset = self.prepare_pin(self.PIN_ID_FOR_LORA_RESET)        
        self.reset_pin(self.pin_reset)
        self.spi = self.prepare_spi(self.get_spi())        
        self.transceivers = {}

        
    def get_spi(self): 
        
        # spi = SPI(id, baudrate = 10000000, polarity = 0, phase = 0)
        # spi.init()
            
        spi = SPI(-1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                    sck = Pin(self.PIN_ID_SCK, Pin.OUT, Pin.PULL_DOWN),
                    mosi = Pin(self.PIN_ID_MOSI, Pin.OUT, Pin.PULL_UP),
                    miso = Pin(self.PIN_ID_MISO, Pin.IN, Pin.PULL_UP))
        spi.init()
            

        
        return spi
    def add_transceiver(self, transceiver):
        
        transceiver.transfer = self.spi.transfer

        
        transceiver.pin_ss = self.prepare_pin(self.PIN_ID_FOR_LORA_SS)
        transceiver.pin_RxDone = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO0)
        transceiver.pin_RxTimeout = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO1)
        transceiver.pin_ValidHeader = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO2)
        transceiver.pin_CadDone = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO3)
        transceiver.pin_CadDetected = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO4)
        transceiver.pin_PayloadCrcError = self.prepare_irq_pin(self.PIN_ID_FOR_LORA_DIO5)
        
        transceiver.init()        
        self.transceivers[transceiver.name] = transceiver 
        return transceiver
        
                 
    def prepare_pin(self, pin_id, in_out = Pin.OUT):
        if pin_id is not None:
            pin = Pin(pin_id, in_out)
            new_pin = Controller.Mock()
            new_pin.pin_id = pin_id
            new_pin.value = pin.value
            
            if in_out == Pin.OUT:
                new_pin.low = lambda : pin.value(0)
                new_pin.high = lambda : pin.value(1)        
            else:
                new_pin.irq = pin.irq 
                
            return new_pin


    def prepare_irq_pin(self, pin_id): 
        pin = self.prepare_pin(pin_id, Pin.IN) 
        if pin:
            pin.set_handler_for_irq_on_rising_edge = lambda handler: pin.irq(handler = handler, trigger = Pin.IRQ_RISING)
            pin.detach_irq = lambda : pin.irq(handler = None, trigger = 0)
            return pin
            
        
        

        
        
    def prepare_spi(self, spi): 
        if spi:
            new_spi = Controller.Mock()  

            def transfer(pin_ss, address, value = 0x00):        
                response = bytearray(1)

                pin_ss.low()
                 
                spi.write(bytes([address]))
                spi.write_readinto(bytes([value]), response)

                pin_ss.high()

                return response
                
            new_spi.transfer = transfer
            new_spi.close = spi.deinit            
            return new_spi
            





    def reset_pin(self, pin, duration_low = 0.05, duration_high = 0.05):
        pin.low()
        sleep(duration_low)
        pin.high()
        sleep(duration_high)
        
        
    def __exit__(self): 
        self.spi.close()        




