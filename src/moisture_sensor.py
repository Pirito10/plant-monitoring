import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Creamos el bus I2C
i2c = board.I2C()

# Creamos el objecto ADC
ads = ADS1115(i2c)

# Creamos el canal analógico para el sensor de humedad
chan = AnalogIn(ads, ads1x15.A0)

# Función para leer la humedad del suelo
def read_soil_moisture():
    return chan.value, chan.voltage