'''
# RPi_I2C_driver - TEST program

# The circuit:
# RaspberryPi       - 1602 I2C LCD
# Vcc               - Vcc
# GND               - GND
# GPIO02 (PIN3/SDA) - SDA
# GPIO03 (PIN5/SCL) - SCL
# 
# ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended.

# by eleparts (yeon) (https://www.eleparts.co.kr/)
# 2019-06-25
'''
import RPi_I2C_driver
from time import *
import RPi.GPIO as GPIO
from multiprocessing import Process

GPIO.setwarnings(False)

SW = 15
trig = 7
echo = 11
buz=13    
    
def LCDThank():
    lcd.clear()
    lcd.noCursor()
    lcd.print("THANK YOU")
    sleep(0.5)
        
def distan():
    GPIO.output(trig,GPIO.LOW)
    sleep(0.5)
    GPIO.output(trig,GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(trig,GPIO.LOW)
    
    while (GPIO.input(echo) == GPIO.LOW):
        start_time = time()
    while (GPIO.input(echo) == GPIO.HIGH):
        end_time= time()
    
    distance = (end_time-start_time)*34000/2
    
    print("distance = %.2f cm" % distance)
    
    if distance <= 20 :
        GPIO.output(buz,GPIO.HIGH)
    else:
        GPIO.output(buz,GPIO.LOW)


    
eleLogo1 = [
  0b00000,
  0b00000,
  0b00110,
  0b01001,
  0b10001,
  0b10000,
  0b10000,
  0b01110
]

eleLogo2 = [
  0b00011,
  0b00100,
  0b01001,
  0b01010,
  0b10010,
  0b10001,
  0b00000,
  0b00000
]
eleLogo3 = [
  0b00000,
  0b10000,
  0b00110,
  0b01001,
  0b01000,
  0b10000,
  0b00000,
  0b00000
]

eleLogo4 = [
  0b00000,
  0b00000,
  0b00000,
  0b00000,
  0b10000,
  0b01000,
  0b01000,
  0b10000
]

eleLogo5 = [
  0b00010,
  0b00100,
  0b00100,
  0b00010,
  0b00001,
  0b00000,
  0b00000,
  0b00000
]

eleLogo6 = [
  0b00000,
  0b00000,
  0b00011,
  0b00100,
  0b00100,
  0b11001,
  0b00010,
  0b00001
]

eleLogo7 = [
  0b00000,
  0b00000,
  0b00000,
  0b10011,
  0b10101,
  0b00100,
  0b01000,
  0b10000
]

eleLogo8 = [
  0b11000,
  0b00100,
  0b00010,
  0b00010,
  0b00100,
  0b11000,
  0b00000,
  0b00000
]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SW,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(buz,GPIO.OUT,initial=GPIO.LOW)

lcd = RPi_I2C_driver.lcd(0x27)

lcd.cursor()
while 1:
    lcd.clear()
    lcd.print("Good day!")
    sleep(0.5)
    key_in = GPIO.input(SW)
    Process(target=distan).start()
    if key_in == 0:
        LCDThank()
        lcd.clear()
        
GPIO.cleanup()

