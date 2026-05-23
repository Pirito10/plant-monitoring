import RPi.GPIO as GPIO


class LedRGB:
    # Inicializamos el LED RGB
    def __init__(self, pin_r, pin_g, pin_b, pwm_freq, optimal):
        # Inicializamos los pines GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_r, GPIO.OUT)
        GPIO.setup(pin_g, GPIO.OUT)
        GPIO.setup(pin_b, GPIO.OUT)

        # Configuramos la frecuencia PWM para cada color
        self.pwm_r = GPIO.PWM(pin_r, pwm_freq)
        self.pwm_g = GPIO.PWM(pin_g, pwm_freq)
        self.pwm_b = GPIO.PWM(pin_b, pwm_freq)

        # Apagamos el LED al inicio
        self.pwm_r.start(0)
        self.pwm_g.start(0)
        self.pwm_b.start(0)

        # Guardamos el valor óptimo de humedad
        self.optimal = optimal

    # Función para calcular el color RGB para un valor de humedad
    def _moisture_to_color(self, moisture):
        # Convertimos la humedad a un valor entre 0 y 1
        m = max(0, min(100, moisture)) / 100
        # Convertimos el valor óptimo a un valor entre 0 y 1
        opt = max(0, min(100, self.optimal)) / 100

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
    def _set_color(self, r, g, b):
        # Ajustamos los valores PWM para cada color
        self.pwm_r.ChangeDutyCycle(r / 255 * 100)
        self.pwm_g.ChangeDutyCycle(g / 255 * 100)
        self.pwm_b.ChangeDutyCycle(b / 255 * 100)

    # Función para actualizar el color del LED
    def update(self, moisture):
        # Calculamos el color basado en la humedad
        r, g, b = self._moisture_to_color(moisture)
        # Establecemos el color del LED
        self._set_color(r, g, b)
