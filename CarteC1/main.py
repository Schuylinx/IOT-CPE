from microbit import *
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

initialize(pinReset=pin0)

while True :
    clear_oled()
    add_text(0, 0, "Temp : "+str(temperature())+" C")
    add_text(0, 1, "Lum : "+str(int((display.read_light_level()/255)*100))+" %")
    sleep(20000)