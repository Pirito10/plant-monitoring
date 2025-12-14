import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Creamos el bus I2C
i2c = board.I2C()

# Creamos el objecto ADC
ads = ADS1115(i2c)

# Creamos el canal analógico para el sensor de humedad
chan = AnalogIn(ads, ads1x15.Pin.A0)

# Función para leer el valor bruto del sensor de humedad
def read_raw():
    return chan.value

# Función para convertir un valor bruto a humedad relativa normalizada
def raw_to_moisture(raw, raw_dry, raw_wet):
    # Calculamos la humedad relativa normalizada
    moisture = (raw_dry - raw) / (raw_dry - raw_wet)
    # Devolvemos el valor entre 0 y 1
    return max(0, min(1, moisture))

# Función para leer la humedad del suelo en porcentaje
def read_soil_moisture(raw_dry, raw_wet):
    # Leemos el valor bruto del sensor
    raw = read_raw()
    # Devolvemos el valor bruto convertido a humedad relativa en porcentaje
    return raw_to_moisture(raw, raw_dry, raw_wet) * 100