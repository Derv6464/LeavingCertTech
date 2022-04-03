import machine 
import utime
led1 = machine.Pin(8, machine.Pin.OUT)

pins = [
    machine.Pin(15,machine.Pin.OUT),
    machine.Pin(14,machine.Pin.OUT),
    machine.Pin(16,machine.Pin.OUT),
    machine.Pin(17,machine.Pin.OUT),
    ]

full_step_sequence = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
    ]

def motorTurn():
    print('motor turning')
    led1.value(1)
    for j in range(24):
        for step in full_step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
                utime.sleep(0.001)
    led1.value(0)



