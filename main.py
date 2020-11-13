from microbit import *
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

initialize()
clear_oled()
add_text(0, 0, "Salut !!!")