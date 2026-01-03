from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

POT = [
    "00000011000",
    "00000111000",
    "00110110110",
    "00111101110",
    "00011101100",
    "01100110000",
    "01110100110",
    "00111101110",
    "00000111100",
    "00000100000",
    "11111111111",
    "11111111111",
    "01111111110",
    "01111111110",
    "01111111110",
    "00111111100",
    "00111111100",
    "00111111100"
]

# Función para inicializar la pantalla
def init():
    # Variables globales
    global device

    # Creamos el bus I2C
    serial = i2c()

    # Creamos el objeto de la pantalla
    device = sh1106(serial)

# Función para dibujar un sprite en la pantalla
def draw_sprite(draw, sprite, x0, y0, scale):
    # Recorremos las filas del sprite
    for y, row in enumerate(sprite):
        # Recorremos los píxeles de la fila
        for x, px in enumerate(row):
            # Si el píxel está activo, lo dibujamos a partir de las coordenadas dadas y con el escalado indicado
            if px == "1":
                draw.rectangle(
                    (
                        x0 + x * scale,
                        y0 + y * scale,
                        x0 + x * scale + scale - 1,
                        y0 + y * scale + scale - 1,
                    ),
                    fill="white"
                )
