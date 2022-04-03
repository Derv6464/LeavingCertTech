import machine
from utime import sleep
buzzer = machine.PWM(machine.Pin(10))
led2 = machine.Pin(9, machine.Pin.OUT) 




def playtone():
    buzzer.duty_u16(6000)
    led2.value(1)
    buzzer.freq(659)
    sleep(0.5)
    led2.value(0)
    buzzer.freq(784)
    sleep(0.5)



def buzbuz(j):
    for i in range(j):
        playtone()
    
    buzzer.duty_u16(0)


