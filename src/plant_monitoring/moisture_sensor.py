import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15


class MoistureSensor:
    # Inicializamos el sensor de humedad
    def __init__(self, pin):
        # Creamos el bus I2C
        i2c = board.I2C()

        # Creamos el objeto ADC
        ads = ADS1115(i2c)

        # Creamos el canal analógico para el sensor de humedad
        self.chan = AnalogIn(ads, getattr(ads1x15.Pin, pin))

    # Función para leer el valor bruto del sensor de humedad
    def read_raw(self):
        return self.chan.value

    # Función para convertir un valor bruto a humedad relativa normalizada
    @staticmethod
    def raw_to_moisture(raw, raw_dry, raw_wet):
        # Calculamos la humedad relativa normalizada
        moisture = (raw_dry - raw) / (raw_dry - raw_wet)
        # Devolvemos el valor entre 0 y 1
        return max(0, min(1, moisture))

    # Función para leer la humedad del suelo en porcentaje
    def read_soil_moisture(self, raw_dry, raw_wet):
        # Leemos el valor bruto del sensor
        raw = self.read_raw()
        # Devolvemos el valor bruto convertido a humedad relativa en porcentaje
        return self.raw_to_moisture(raw, raw_dry, raw_wet) * 100
