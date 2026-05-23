from apscheduler.schedulers.blocking import BlockingScheduler

from plant_monitoring.camera import take_photo
from plant_monitoring.config import load_config
from plant_monitoring.paths import BASE_DIR
from plant_monitoring.moisture_sensor import MoistureSensor
from plant_monitoring.led_rgb import LedRGB
from plant_monitoring.display import Display


def main():
    # Cargamos la configuración
    cfg = load_config()

    # Inicializamos el sensor de humedad
    moisture_sensor = MoistureSensor(cfg["moisture"]["pin"])

    # Inicializamos el LED RGB
    led = LedRGB(
        cfg["led_rgb"]["pins"]["red"],
        cfg["led_rgb"]["pins"]["green"],
        cfg["led_rgb"]["pins"]["blue"],
        cfg["led_rgb"]["pwm_frequency"]
    )

    # Inicializamos la pantalla
    display = Display()

    # Creamos el planificador de tareas
    scheduler = BlockingScheduler()

    # Programamos la toma de fotos
    scheduler.add_job(
        take_photo,
        "cron",
        hour=",".join(map(str, cfg["scheduler"]["photo_hours"])),
        args=[
            BASE_DIR / cfg["paths"]["photos"],
            cfg["camera"]["width"],
            cfg["camera"]["height"]
        ],
    )

    #! ----- Temporal ------
    moisture = 0

    def job_read_moisture():
        nonlocal moisture
        moisture = moisture_sensor.read_soil_moisture(cfg["moisture"]["raw_dry"], cfg["moisture"]["raw_wet"])
        led.update(moisture, cfg["moisture"]["optimal"])

    def job_update_display():
        display.update(moisture, cfg["display"]["moisture_threshold"], cfg["display"]["blink_interval"])
    #! ---------------------

    # Programamos la lectura del sensor de humedad
    scheduler.add_job(
        job_read_moisture,
        "interval",
        seconds=cfg["scheduler"]["moisture_interval"]
    )

    # Programamos la actualización de la pantalla
    scheduler.add_job(
        job_update_display,
        "interval",
        seconds=cfg["scheduler"]["display_interval"]
    )

    # Leemos la humedad al iniciar
    job_read_moisture()

    # Iniciamos el planificador
    scheduler.start()


if __name__ == "__main__":
    main()
