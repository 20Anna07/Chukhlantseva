import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

def adc_1():
    for value in range(256):
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            time.sleep(0.001)
            return value/255*3.3
    return 3.3

def bin2dec(num):
    string = '0b'
    for i in num:
        string += str(i)
    return int(string, base=2)

def adc():
    value = [0]*8
    for i in range(8):
        value[i] = 1
        GPIO.output(dac, value)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 1:
            value[i] = 0
    GPIO.output(dac, value)
    time.sleep(0.01)
    return bin2dec(value)/255*3.3

def dec2bin(num):
    bi = bin(int(num))[2:].zfill(8)
    result = list(map(int, bi))
    return result

try:
    measures = []
    time_start = time.time()
    GPIO.output(troyka, GPIO.HIGH)
    while adc() <= 0.7*3.3:
        measures.append(adc())
        GPIO.output(leds, dec2bin(adc()))
        print
    print('разрядка')
    time.sleep(0.01)
    GPIO.output(troyka, GPIO.LOW)
    while adc() >= 0.4*3.3:
        measures.append(adc())
        GPIO.output(leds, dec2bin(adc()))
    time_finish = time.time()
    final_time = time_finish - time_start
    print(f'final_time = {final_time}')

    plt.plot(measures)
    plt.show()
    measures_str = [str(i) for i in measures]
    with open('data.txt', 'w') as outfile:
        outfile.write('\n'.join(measures_str))

finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()
    T = final_time/len(measures)
    n = 1/T
    qs = 3.3/256
    with open('settings.txt', 'w') as out:
        out.write('n = '+str(n)+' qs = '+str(qs))
    print(f'T = {T}, n = {n}, qs = {qs}')
