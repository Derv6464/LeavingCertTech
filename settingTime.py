import machine
import utime
from pico_i2c_lcd import I2cLcd
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

upArrow = bytearray([0x00,0x04,0x0E,0x15,0x04,0x04,0x04,0x00])
downArrow = bytearray([0x00,0x04,0x04,0x04,0x15,0x0E,0x04,0x00])
tick = bytearray([0x00,0x00,0x00,0x01,0x02,0x14,0x08,0x00])
ex = bytearray([0x00,0x00,0x11,0x0A,0x04,0x0A,0x11,0x00])
lcd.custom_char(0, upArrow)
lcd.custom_char(6, downArrow)
lcd.custom_char(2, tick)
lcd.custom_char(3, ex)

downButton = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
upButton = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_DOWN)

yesButton = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_DOWN)



def timeSetHrSingle(info,hr):
    lcd.clear()
    lcd.putstr(info)
    lcd.putstr("           "+chr(0))
    lcd.putstr("        Hours:     "+str(hr)+'  '+chr(2))
    lcd.putstr("                "+chr(6))
    
def timeSetHrDouble(info,hr):
    lcd.clear()
    lcd.putstr(info)
    lcd.putstr("           "+chr(0))
    lcd.putstr("        Hours:     "+str(hr)+'  '+chr(2))
    lcd.putstr("               "+chr(6))
    
def timeSetMinSingle(info,mins):
    lcd.clear()
    lcd.putstr(info)
    lcd.putstr("           "+chr(0))
    lcd.putstr("        Minutes:   "+str(mins)+'  '+chr(2))
    lcd.putstr("                "+chr(6))

def timeSetMinDouble(info,mins):
    lcd.clear()
    lcd.putstr(info)
    lcd.putstr("          "+chr(0))
    lcd.putstr("         Minutes:   "+str(mins)+'  '+chr(2))
    lcd.putstr("              "+chr(6))
    
    
# timeSetHrSingle(hr)
#  0 is hr, 1 is min
# timeMode = 0

def setTime(info):
    hr = 0
    mins = 0
    timeSetHrSingle(info,hr)
    timeMode = 0
    #hrs
    while yesButton.value()!=1 and timeMode==0:
        utime.sleep(0.2)
        if upButton.value()==1 and timeMode==0:
            hr += 1
            if hr > 23:
                hr=0
            #print(hr)
            if hr < 10:
                timeSetHrSingle(info,hr)
            else:
                timeSetHrDouble(info,hr)
            utime.sleep(0.2)
        if downButton.value()==1 and timeMode==0:
            hr -= 1
            if hr < 0:
                hr=23
            #print(hr)
            if hr < 10:
                timeSetHrSingle(info,hr)
            else:
                timeSetHrDouble(info,hr)
            utime.sleep(0.2)
        if yesButton.value()==1 and timeMode==0:
            print('yo?')
            timeMode = 1
            timeSetMinSingle(info,mins)
            utime.sleep(0.2)
            
#     mins
    print('hr done',timeMode)
    while yesButton.value()!=1 and timeMode==1:
        utime.sleep(0.2)
        if upButton.value()==1 and timeMode==1:
            mins += 1
            if mins > 59:
                mins=0
            #print(mins)
            if mins < 10:
                timeSetMinSingle(info,mins)
            else:
                timeSetMinDouble(info,mins)
            utime.sleep(0.2)
        if downButton.value()==1 and timeMode==1:
            mins -= 1
            if mins < 0:
                mins=59
            #print(hr)
            if hr < 10:
                timeSetMinSingle(info,mins)
            else:
                timeSetMinDouble(info,mins)
            utime.sleep(0.2)
        if yesButton.value()==1 and timeMode==1:
            utime.sleep(0.2)
            print(hr,mins)
            if hr == 0 and mins == 0:
                return(0,0)
            elif hr == 0:
                return(0,mins)
            elif mins == 0:
                return(hr,0)
            else:
                return(hr,mins)
    print('min done',timeMode)
#     set 3 times
    
def runTimes():
    times = ["Set current time    ","Set 1st dispense    ","Set 2nd dispense    ","Set 3rd dispense    "]
    timesSet = []
    for i in times:
        j = setTime(i)
        print(j)
        timesSet.append(j)
    return(timesSet)    

