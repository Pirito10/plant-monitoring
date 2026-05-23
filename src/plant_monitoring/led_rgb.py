from gpiozero import RGBLED


class LedRGB:
    # Inicializamos el LED RGB
    def __init__(self, pin_r, pin_g, pin_b, optimal_moisture):
        # Inicializamos el LED RGB
        self.led = RGBLED(red=pin_r, green=pin_g, blue=pin_b)

        # Guardamos el valor óptimo de humedad
        self.optimal_moisture = optimal_moisture

    # Función para calcular el color RGB para un valor de humedad
    def _moisture_to_color(self, moisture):
        # Convertimos la humedad a un valor entre 0 y 1
        m = max(0, min(100, moisture)) / 100
        # Convertimos el valor óptimo a un valor entre 0 y 1
        opt = max(0, min(100, self.optimal_moisture)) / 100

        # Si hay humedad baja, el color sale entre rojo y verde
        if m <= opt:
            # Calculamos el punto dentro del rango
            t = m / opt
            # Calculamos los valores RGB
            r = 1 - t
            g = t
            b = 0.0

        # Si hay humedad alta, el color sale entre verde y azul
        else:
            # Calculamos el punto dentro del rango
            t = (m - opt) / (1 - opt)
            # Calculamos los valores RGB
            r = 0.0
            g = 1 - t
            b = t

        # Devolvemos los valores RGB
        return r, g, b

    # Función para establecer el color del LED RGB
    def _set_color(self, r, g, b):
        self.led.color = (r, g, b)

    # Función para actualizar el color del LED
    def update(self, moisture):
        # Calculamos el color basado en la humedad
        r, g, b = self._moisture_to_color(moisture)
        # Establecemos el color del LED
        self._set_color(r, g, b)
