from time import sleep_ms, sleep, time
from machine import Pin, SPI, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from mfrc522 import MFRC522
import network
from os import uname
import urequests, ujson


IP = "192.168.187.183"

YES = Pin(16, Pin.IN)


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

red = Pin(17, Pin.OUT)
green = Pin(4, Pin.OUT)

sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(2, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda = Pin(5, Pin.OUT)


def lcd_print(string, clear=True):
	if clear:
		lcd.clear()
	lcd.putstr("\n\n"+string)


items_List = set()


def main():

    try:
        while True:
            try:
                addItem = addingMode()
            except:
                print("Can't connect to server")
            rdr = MFRC522(spi, sda)
            (stat, tag_type) = rdr.request(rdr.REQIDL)
            if stat == rdr.OK:
                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("Tag ID: " + str(uid))
                    items_List.add(uid)
                    if addItem:
                        try:
                            send_item(uid)
                        except:
                            print("Can't connect to server")
                    else:
                        print("TESTING ISONSHELF")
                        try:
                            on_shelf = isItemOnShelf(uid)
                            print(f"on shelf ?: {on_shelf}")
                        except:
                            print("Can't connect to server")
            else:
                print("TESTING ISONSHELF")
                if len(items_List) > 0:
                    for el in items_List:
                        items_List.remove(el)
                        on_shelf = isItemOnShelf(el)
                        print(f"on shelf ?: {on_shelf}")
                        if not on_shelf:
                            itemsPicked(el)
            sleep_ms(100)
            print("Waiting....")
    except KeyboardInterrupt:
        print("Bye")

def itemsPicked(args):
    r = urequests.get(url=f'http://{IP}:5000/picked/{args}?')
    
    items_picked = ujson.loads(r.content)["items_picked"]
    r.close()

    return items_picked

def isItemOnShelf(id):
     r = urequests.get(url=f'http://{IP}:5000/getItem/{id}')
     items = ujson.loads(r.content)

     print(items)

     r.close()
     if len(items) > 0 and id in items_List:
        return True
     else:
        return False
          
          

def checkNumberItems():
     return False

def send_item(uid):
    tag_id = str(uid)
    r = urequests.get(url=f"http://{IP}:5000/addtag?tag_id={tag_id}")
    r.close()

def addingMode():
    r = urequests.get(url=f'http://{IP}:5000/mode')
    r.close()
      
    if r.status_code == 403:
        return False
    
    return True

main()

sta_if.disconnect()
