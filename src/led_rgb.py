import RPi.GPIO as GPIO

# Definimos los pines para el LED RGB
PIN_R = 17
PIN_G = 27
PIN_B = 22

# Definimos la frecuencia de PWM
PWM_FREQ = 500

# Inicializamos los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_R, GPIO.OUT)
GPIO.setup(PIN_G, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)

# Configuramos PWM para cada pin
pwm_r = GPIO.PWM(PIN_R, PWM_FREQ)
pwm_g = GPIO.PWM(PIN_G, PWM_FREQ)
pwm_b = GPIO.PWM(PIN_B, PWM_FREQ)

# Apagamos el LED al inicio
pwm_r.start(0)
pwm_g.start(0)
pwm_b.start(0)

# Función para calcular el color RGB para un valor de humedad
def moisture_to_color(moisture, optimal):
    # Convertimos la humedad a un valor entre 0 y 1
    m = max(0, min(100, moisture)) / 100
    # Convertimos el valor óptimo a un valor entre 0 y 1
    opt = max(0, min(100, optimal)) / 100

    # Si hay humedad baja, el color sale entre rojo y verde
    if m <= opt:
        # Calculamos el punto dentro del rango
        t = m / opt
        # Calculamos los valores RGB
        r = int(255 * (1 - t))
        g = int(255 * t)
        b = 0

    # Si hay humedad alta, el color sale entre verde y azul
    else:
        # Calculamos el punto dentro del rango
        t = (m - opt) / (1 - opt)
        # Calculamos los valores RGB
        r = 0
        g = int(255 * (1 - t))
        b = int(255 * t)

    # Devolvemos los valores RGB
    return r, g, b

# Función para establecer el color del LED RGB
def set_color(r, g, b):
    # Ajustamos los valores PWM para cada color
    pwm_r.ChangeDutyCycle(r / 255 * 100)
    pwm_g.ChangeDutyCycle(g / 255 * 100)
    pwm_b.ChangeDutyCycle(b / 255 * 100)

# Función para actualizar el color del LED
def update_led(moisture, optimal):
    # Calculamos el color basado en la humedad
    r, g, b = moisture_to_color(moisture, optimal)
    # Establecemos el color del LED
    set_color(r, g, b)