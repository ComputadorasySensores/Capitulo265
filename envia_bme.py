import network
import espnow
import time
from machine import Pin, I2C
import bme280

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Fallo de inicialización ESP-NOW:", err)
    raise

mac_receptor = b'\xff\xff\xff\xff\xff\xff'

try:
    e.add_peer(mac_receptor)
except OSError as err:
    print("Fallo al agregar el par (peer):", err)
    raise

i2c = I2C(0, scl=Pin(9), sda=Pin(8))
sensor = bme280.BME280(i2c=i2c)

contador = 1
while True:
    try:
        t, p, h = sensor.read_compensated_data()
        mensaje = f"{t:.1f}C, {h:.1f}%, {p/100:.1f}hPa"
        try:
            if e.send(mac_receptor, mensaje, True):
                print(f"Mensaje: {mensaje}")
            else:
                print("Fallo en envío de mensaje")
        except OSError as err:
            print(f"Fallo general (OSError: {err})")
        
        contador += 1
        
        time.sleep(10) 
        
    except OSError as err:
        print("Error:", err)
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Deteniendo ...")
        e.active(False)
        sta.active(False)
        break