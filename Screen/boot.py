from time import sleep_ms, sleep, time
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import network
import urequests, ujson


IP = "192.168.187.183"

YES = Pin(16, Pin.IN)
NO = Pin(17, Pin.IN)

I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns) 



items_picked = 0

ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)

sta_if = network.WLAN(network.STA_IF)


connected = sta_if.isconnected()


if not connected:
    sta_if.active(True)
    sta_if.connect("ESP", "esp32_123")
    print("No connection :(") 

    while not sta_if.isconnected():
        pass

print("Connected: " + str(sta_if.isconnected()))

def itemsPicked(args):
    try:
        r = urequests.get(url=f'http://{IP}:5000/picked?{args}')
        
        items_picked = ujson.loads(r.content)["items_picked"]
        print(items_picked)
        r.close()

        return items_picked
    except:
        return -1


def lcd_print(string, clear=True):
    if clear:
        lcd.clear()
    lcd.putstr("\n\n" + string)


picked_up_start = False
start = 0

def send_notification(message):
    try:
        r = urequests.get(url=f'http://{IP}:5000/notification?message={message}')        
        r.close()
    except:
        return -1


yes = False
no = False

args = ""

while True:
    
    yes = YES.value()

    print("args: "+ args)


    items_picked = itemsPicked(args)

    s = ""

    if not picked_up_start:
         start = time()

    if items_picked > 0:
        picked_up_start = True

        if items_picked > 1:
            s = "s"
        lcd_print(f"Items picked up: {items_picked}?")

        if yes:
            args = "status=yes"
            itemsPicked(args)
            args = ""
            yes = False
            lcd_print("APPROVED")
            sleep_ms(2000)
            lcd.clear()
        elif no:
            args = "status=no"
            no = False
        else:
            end = time()
            if (end - start) == 30: #5 minutes in seconds
                send_notification("Problem with inventory !")
             

    #sleep_ms(300)
