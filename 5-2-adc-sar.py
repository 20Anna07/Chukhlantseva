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

def bin2dec(num):
    string = '0b'
    for i in num:
        string += str(i)
    return int(string, base=2)

def adc_sar():
    value = [0]*8
    for i in range(8):
        value[i] = 1
        GPIO.output(dac, value)
        time.sleep(0.1)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            value[i] = 0
    GPIO.output(dac, value)
    time.sleep(0.01)
    return bin2dec(value)

try:
    while True:
        adc_v = adc_sar()
        voltage = adc_v/256*3.3
        print(f'voltage = {voltage}, value = {adc_v}')
        time.sleep(2)
        
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()