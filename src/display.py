import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

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

DROP = [
    "00000100000",
    "00000100000",
    "00000100000",
    "00001010000",
    "00001010000",
    "00001010000",
    "00010001000",
    "00010001000",
    "00100000100",
    "00100000100",
    "01000000010",
    "01000000010",
    "10000000001",
    "10100000001",
    "10100000001",
    "01010000010",
    "01001100010",
    "00110001100",
    "00001110000"
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

# Función para dibujar una barra de progreso en la pantalla
def draw_bar(draw, percent, x, y, width, height):
    # Convertimos el porcentaje a un valor entre 0 y 1
    p = max(0, min(100, percent)) / 100
    # Calculamos el ancho sin contar el borde
    fill_width = p * (width - 2)

    # Dibujamos el borde
    draw.rectangle((x, y, x + width, y + height), outline="white")

    # Dibujamos el relleno
    if fill_width > 0:
        draw.rectangle((x + 1, y + 1, x + 1 + fill_width, y + height - 1), fill="white")

# Función para actualizar la pantalla
def update_display(moisture, moisture_threshold, blink_interval):
    # Determinamos si la gota debe parpadear
    blink = moisture < moisture_threshold

    # Si la humedad es muy baja, aumentamos la frecuencia de parpadeo
    effective_interval = blink_interval
    if moisture < moisture_threshold / 2:
        effective_interval = blink_interval / 2

    # Determinamos si la gota se debe mostrar
    if blink:
        drop_on = (int(time.monotonic() / effective_interval) % 2) == 0

    # Dibujamos en la pantalla
    with canvas(device) as draw:
        # Dibujamos el sprite de la planta
        draw_sprite(draw, POT, 0, 0, 3)
        # Dibujamos una barra con el nivel de humedad
        draw_bar(draw, moisture, 0, 57, 33, 5)
        # Dibujamos el valor de humedad
        draw.text((37, 54), f"{round(moisture)}%", fill="white")
        # Dibujamos el sprite de la gota según el parpadeo
        if not blink or drop_on:
            draw_sprite(draw, DROP, 60, 0, 3)