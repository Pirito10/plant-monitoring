import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15


class MoistureSensor:
    # Inicializamos el sensor de humedad
    def __init__(self, pin, raw_dry, raw_wet):
        # Creamos el bus I2C
        i2c = board.I2C()

        # Creamos el objeto ADC
        ads = ADS1115(i2c)

        # Creamos el canal analógico para el sensor de humedad
        self.chan = AnalogIn(ads, getattr(ads1x15.Pin, pin))

        # Guardamos los valores de calibración
        self.raw_dry = raw_dry
        self.raw_wet = raw_wet

    # Función para leer el valor bruto del sensor de humedad
    def _read_raw(self):
        return self.chan.value

    # Función para convertir un valor bruto a humedad relativa normalizada
    def _raw_to_moisture(self, raw):
        # Calculamos la humedad relativa normalizada
        moisture = (self.raw_dry - raw) / (self.raw_dry - self.raw_wet)
        # Devolvemos el valor entre 0 y 1
        return max(0, min(1, moisture))

    # Función para leer la humedad del suelo en porcentaje
    def read_soil_moisture(self):
        # Leemos el valor bruto del sensor
        raw = self._read_raw()
        # Devolvemos el valor bruto convertido a humedad relativa en porcentaje
        return self._raw_to_moisture(raw) * 100
