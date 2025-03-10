import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    bi = bin(num)[2:].zfill(8)
    result = list(map(int, bi))
    return result

def adc():
    for value in range(256):
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            time.sleep(3)
            return value
    return 255

try:
    while True:
        adc_v = adc()
        voltage = adc_v/256*3.3
        print(f'voltage = {voltage}, value = {adc_v}')
        time.sleep(5)
        
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
