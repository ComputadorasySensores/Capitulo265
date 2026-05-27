import network
import espnow
import time
from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def actualizar_pantalla(texto):
    oled.fill(0)
    oled.text("Datos BME280", 15, 0)
    lineas = texto.split(", ")
    y = 20
    for linea in lineas:
        oled.text(linea, 0, y)
        y += 15
    oled.show()

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Fallo de inicialización ESP-NOW:", err)
    raise

print("En espera de mensajes ...")
oled.fill(0)
oled.text("Esperando datos", 0, 40)
oled.show()
while True:
    try:
        host, msg = e.recv(10000)
        if msg:
            print(f"Recibido de {host.hex()}: {msg.decode()}")
            datos = msg.decode('utf-8')
            actualizar_pantalla(datos)
        
    except OSError as err:
        print("Error:", err)
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Deteniendo ...")
        e.active(False)
        sta.active(False)

        break
