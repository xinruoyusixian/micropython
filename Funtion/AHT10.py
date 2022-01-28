
import utime

class AHT10:
    def __init__(self, i2c, address=0x38):
        if i2c is None:
            raise ValueError('I2C object required.')
        self.i2c = i2c
        self.address = address
        self.i2c.writeto(self.address, b'\xE1\x08\x00')  # 初始化模块

        self._h, self._t = 0, 0  # 湿度，温度



    def status(self, data=None):

        '检查忙闲状态'

        if not data:

            self.i2c.writeto(self.address, b'\x71')

            data = self.i2c.readfrom(self.address, 1)
        return data & 0x40  # 最高位为1是忙（测量中）

    def measure(self):
        '测量'
        self._h, self._t = 0, 0
        for _ in range(3): # 最多重试3次
            self.i2c.writeto(self.address, b'\xAC\x33\x00')
            utime.sleep_ms(100)  # 模块需要80ms以上的测量时间
            raw = self.i2c.readfrom(self.address, 6)
            if self.status(raw[0]):
                utime.sleep_ms(20)  # 忙就稍等再测
            else:
                data_h = raw[1] << 12 | raw[2] << 4 | raw[3] >> 4
                data_t = (raw[3] & 0x0F) << 16 | raw[4] << 8 | raw[5]
                self._h, self._t = data_h * 100 / 1048576, ((200 * data_t) / 1048576) - 50
                break


    def humidity(self):
        '返回测量到的湿度 %RH'
        return self._h

    def temperature(self):
        '返回测量到的温度 C'
        return self._t

    def reset(self):
        '软复位'
        self.i2c.writeto(self.address, b'\xBA')
        utime.sleep_ms(20)


