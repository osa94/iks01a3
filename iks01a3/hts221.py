from smbus2 import SMBus


class HTS221(SMBus):

    # registers
    WHO_AM_I = 0x0F
    AV_CONF = 0x10
    CTRL_REG1 = 0x20
    CTRL_REG2 = 0x21
    CTRL_REG3 = 0x22
    STATUS_REG = 0x27
    HUMIDITY_OUT_L = 0x28
    HUMIDITY_OUT_H = 0x29
    TEMPERATURE_OUT_L = 0x2A
    TEMPERATURE_OUT_H = 0x2B

    # calibration registers (humidity)
    H0_rH_x2 = 0x30
    H1_rH_x2 = 0x31
    H0_T0_OUT_H = 0x37
    H0_T0_OUT_L = 0x36
    H1_T0_OUT_H = 0x3B
    H1_T0_OUT_L = 0x3A

    # calibration registers (temperature)
    T0_degC_x8 = 0x32
    T1_degC_x8 = 0x33
    T1_T0_MSB = 0x35
    T0_OUT_H = 0x3C
    T0_OUT_L = 0x3D
    T1_OUT_H = 0x3E
    T1_OUT_L = 0x3F

    # other values
    DEVICE_ADDRESS = 0x5F
    WHO_AM_I_VALUE = 0xBC

    def __init__(self, bus, force=False):
        super().__init__(bus, force)
        self.__h0_t0_out_val = self.__read_h0_t0_out()
        self.__h1_t0_out_val = self.__read_h1_t0_out()
        self.__h0_rh_val = self.__read_h0_rh_x2() / 2
        self.__h1_rh_val = self.__read_h1_rh_x2() / 2
        self.__t0_deg_val = self.__read_t0_deg_x8() / 8
        self.__t1_deg_val = self.__read_t1_deg_x8() / 8
        self.__t0_out_val = self.__read_t0_out()
        self.__t1_out_val = self.__read_t1_out()

    def who_am_i(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.WHO_AM_I)

    def is_detected(self):
        return self.who_am_i() == self.WHO_AM_I_VALUE

    def power_on(self):
        reg_val = self.read_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1)
        reg_val |= 0x80
        self.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, reg_val)

    def power_off(self):
        reg_val = self.read_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1)
        reg_val &= 0x7F
        self.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, reg_val)

    def set_bdu(self, bdu=0):
        reg_val = self.read_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1)
        if bdu:
            reg_val |= 0x04
        else:
            reg_val &= 0xFB
        self.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, reg_val)

    def set_odr(self, odr=(1, 1)):
        reg_val = self.read_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1)
        if odr[0]:
            reg_val |= 0x02
        else:
            reg_val &= 0xFD
        self.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, reg_val)

        if odr[1]:
            reg_val |= 0x01
        else:
            reg_val &= 0xFE
        self.write_byte_data(self.DEVICE_ADDRESS, self.CTRL_REG1, reg_val)

    def __read_humidity_raw_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.HUMIDITY_OUT_H)

    def __read_humidity_raw_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.HUMIDITY_OUT_L)

    def read_humidity_raw(self):
        hum_high = self.__read_humidity_raw_h()
        hum_low = self.__read_humidity_raw_l()
        hum = (-(hum_high & 0x80) + (hum_high & 0x7F)) * 256 + hum_low
        return hum

    def __read_temperature_raw_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.TEMPERATURE_OUT_H)

    def __read_temperature_raw_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.TEMPERATURE_OUT_L)

    def read_temperature_raw(self):
        temp_high = self.__read_temperature_raw_h()
        temp_low = self.__read_temperature_raw_l()
        temp = (-(temp_high & 0x80) + (temp_high & 0x7F)) * 256 + temp_low
        return temp

    def __read_h0_rh_x2(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H0_rH_x2)

    def __read_h1_rh_x2(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H1_rH_x2)

    def __read_t0_deg_x8(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T0_degC_x8)

    def __read_t1_deg_x8(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T1_degC_x8)

    def __read_h0_t0_out_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H0_T0_OUT_H)

    def __read_h0_t0_out_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H0_T0_OUT_L)

    def __read_h0_t0_out(self):
        high = self.__read_h0_t0_out_h()
        low = self.__read_h0_t0_out_l()
        val = (-(high & 0x80) + (high & 0x7F)) * 256 + low
        return val

    def __read_t0_out_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T0_OUT_H)

    def __read_t0_out_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T0_OUT_L)

    def __read_t0_out(self):
        high = self.__read_t0_out_h()
        low = self.__read_t0_out_l()
        val = (-(high & 0x80) + (high & 0x7F)) * 256 + low
        return val

    def __read_h1_t0_out_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H1_T0_OUT_H)

    def __read_h1_t0_out_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.H1_T0_OUT_L)

    def __read_h1_t0_out(self):
        high = self.__read_h1_t0_out_h()
        low = self.__read_h1_t0_out_l()
        val = (-(high & 0x80) + (high & 0x7F)) * 256 + low
        return val

    def __read_t1_out_h(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T1_OUT_H)

    def __read_t1_out_l(self):
        return self.read_byte_data(self.DEVICE_ADDRESS, self.T1_OUT_L)

    def __read_t1_out(self):
        high = self.__read_t1_out_h()
        low = self.__read_t1_out_l()
        val = (-(high & 0x80) + (high & 0x7F)) * 256 + low
        return val

    def read_humidity(self):
        val1 = self.__h1_rh_val - self.__h0_rh_val
        val2 = self.read_humidity_raw() - self.__h0_t0_out_val
        val3 = self.__h1_t0_out_val - self.__h0_t0_out_val
        return (val1 * val2) / val3 + self.__h0_rh_val

    def read_temperature(self):
        val1 = self.__t1_deg_val - self.__t0_deg_val
        val2 = self.read_temperature_raw() - self.__t0_out_val
        val3 = self.__t1_out_val - self.__t0_out_val
        return (val1 * val2) / val3 + self.__t0_deg_val