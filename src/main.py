from apscheduler.schedulers.blocking import BlockingScheduler

from src import config, camera, moisture_sensor, led_rgb, display

# Cargamos la configuración
cfg = config.load_config()

# Inicializamos el sensor de humedad
moisture_sensor.init(cfg["moisture"]["pin"])

# Inicializamos el LED RGB
led_rgb.init(
    cfg["led_rgb"]["pins"]["red"],
    cfg["led_rgb"]["pins"]["green"],
    cfg["led_rgb"]["pins"]["blue"],
    cfg["led_rgb"]["pwm_frequency"]
)

# Inicializamos la pantalla
display.init()

# Creamos el planificador de tareas
scheduler = BlockingScheduler()

# Programamos la toma de fotos
scheduler.add_job(
    camera.take_photo,
    "cron",
    hour=",".join(map(str, cfg["scheduler"]["photo_hours"])),
    args=[
        cfg["paths"]["photos"],
        cfg["camera"]["width"],
        cfg["camera"]["height"]
    ],
)

#! Temporal
def job_read_moisture():
    global moisture
    moisture = moisture_sensor.read_soil_moisture(cfg["moisture"]["raw_dry"], cfg["moisture"]["raw_wet"])
    led_rgb.update_led(moisture, cfg["moisture"]["optimal"])
    print(f"Humedad suelo: {moisture:5.1f}%")

def job_update_display():
    display.update_display(moisture, cfg["display"]["moisture_threshold"], cfg["display"]["blink_interval"])

# Programamos la lectura del sensor de humedad
scheduler.add_job(
    job_read_moisture,
    "interval",
    seconds=cfg["scheduler"]["moisture_interval"]
)

scheduler.add_job(
    job_update_display,
    "interval",
    seconds=cfg["scheduler"]["display_interval"]
)

# Leemos la humedad al iniciar
job_read_moisture()

# Iniciamos el planificador
scheduler.start()