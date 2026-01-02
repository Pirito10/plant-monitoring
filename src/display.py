from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

# Función para inicializar la pantalla
def init():
    # Variables globales
    global device

    # Creamos el bus I2C
    serial = i2c()

    # Creamos el objeto de la pantalla
    device = sh1106(serial)