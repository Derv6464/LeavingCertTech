import machine
import utime
from pico_i2c_lcd import I2cLcd
from settingTime import runTimes
from motorTurning import motorTurn
from buzzerAlarm import buzbuz
import displays

i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)
rtc = machine.RTC()

downButton = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
upButton = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_DOWN)
noButton = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)
yesButton = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_DOWN)
testButton = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN)
onSwitch = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN)
led1 = machine.Pin(8, machine.Pin.OUT)
led1.value(0)
led2 = machine.Pin(9, machine.Pin.OUT)
led2.value(0)
buzzer = machine.PWM(machine.Pin(10))
buzzer.duty_u16(0)
ldr = machine.ADC(27)
    
def changeStart(level):
    if level == 0:
        displays.startMenu1()
    else:
        displays.startMenu2()
        
def changeSetting(level2):
    if level2 == 0:
        displays.settingMenu1()
    else:
        displays.settingMenu2() 

def dispense():
    motorTurn()
    buzbuz(10)
    displays.pillOut()
    
    if not demoAlarmWait():
        while ldrCheck() == False:
            buzbuz(1)
            if noButton.value()==1:
                print('canceled')
                break
        print('pickedup')
        displays.thanks()
        utime.sleep(10)
        if mode ==1:
            displays.demo()
        else:
            updateStart(curHr,curMin)
    else:
        displays.thanks()
        utime.sleep(10)
        if mode ==1:
            displays.demo()
        else:
            updateStart(curHr,curMin)

def ldrCheck():
    print('ldr check',ldr.read_u16())
    if ldr.read_u16() < 400:
        return True
    else:
        return False
    
def demoAlarmWait():
    print('alarm wait')
#   if cup has been pickecd up within 10 sec
    pickUp = False
    for i in range(20):
        utime.sleep(0.5)
        if ldrCheck():
            pickUp=True
            break
    if pickUp:
        return True
    else:
        return False 

def fullStart(rtc):
    times = runTimes()
    print(times)
    if None in times:
        lcd.clear()
        lcd.putstr("error try again")
        utime.sleep(5)
        print('error')
        times = runTimes()
    hr = int(times[0][0])
    mins = int(times[0][1])
    print(hr,mins)
    curTime = times[0][0],times[0][1]
    dose1 = int(times[1][0]),int(times[1][1]),50
    dose2 = int(times[2][0]),int(times[2][1]),50
    dose3 = int(times[3][0]),int(times[3][1]),50
    
    print(curTime,dose1,dose2,dose3)
    return(curTime,dose1,dose2,dose3)

def chooseDose(dose1,dose2,dose3,curHr,curMin):
    doseSend = ''
    print(curHr,curMin)
    print(dose1[0],dose1[1])
    if dose1[0]>= curHr and dose1[1]>= curMin:
        if dose1[0]<10 and dose1[1]<10:
            return(('0'+str(dose1[0]))+':'+('0'+str(dose1[1])))
        elif dose1[0]<10:
            return(('0'+str(dose1[0]))+':'+str(dose1[1]))
        elif dose1[1]<10:
            return(str(dose1[0])+':'+('0'+str(dose1[1])))
        else:
            return(str(dose1[0])+':'+str(dose1[1]))
    elif dose2[0]>=curHr and dose2[1]>=curMin:
        if dose2[0]<10 and dose2[1]<10:
            return(('0'+str(dose2[0]))+':'+('0'+str(dose2[1])))
        elif dose2[0]<10:
            return(('0'+str(dose2[0]))+':'+str(dose2[1]))
        elif dose2[1]<10:
            return(str(dose2[0])+':'+('0'+str(dose2[1])))
        else:
            return(str(dose2[0])+':'+str(dose2[1]))
    elif dose3[0]>=curHr and dose3[1]>=curMin:
        if dose3[0]<10 and dose3[1]<10:
            return(('0'+str(dose3[0]))+':'+('0'+str(dose3[1])))
        elif dose3[0]<10:
            return(('0'+str(dose3[0]))+':'+str(dose3[1]))
        elif dose3[1]<10:
            return(str(dose3[0])+':'+('0'+str(dose3[1])))
        else:
            return(str(dose3[0])+':'+str(dose3[1]))
    else:
        if dose1[0]<10 and dose1[1]<10:
            return(('0'+str(dose1[0]))+':'+('0'+str(dose1[1])))
        elif dose1[0]<10:
            return(('0'+str(dose1[0]))+':'+str(dose1[1]))
        elif dose1[1]<10:
            return(str(dose1[0])+':'+('0'+str(dose1[1])))
        else:
            return(str(dose1[0])+':'+str(dose1[1]))
   
def updateStart(curHr,curMin):
    if curHr < 10 and curMin <10:
        displays.startMenu(('0'+str(curHr)),('0'+str(curMin)),chooseDose(dose1,dose2,dose3,curHr,curMin))
    elif curHr < 10:
        displays.startMenu(('0'+str(curHr)),curMin,chooseDose(dose1,dose2,dose3,curHr,curMin))
    elif curMin <10:
        displays.startMenu(curHr,('0'+str(curMin)),chooseDose(dose1,dose2,dose3,curHr,curMin))
    else:
        displays.startMenu(curHr,curMin,chooseDose(dose1,dose2,dose3))
#0 is start
#1 is demo
#2 is full
mode = 0
level = 0
level2 = 0
if onSwitch.value()==1:
    lcd.backlight_on()
    displays.startMenu1()
while True:
#     if switched on
    if onSwitch.value()==1:

        lcd.backlight_on()
#       if in start mode
        if mode==0:
            if downButton.value()==1:
                level += 1
                if level>1:
                    level= 0
                changeStart(level)
                utime.sleep(0.5)
            if upButton.value()==1:
                level -=1
                if level<0:
                    level=1
                changeStart(level)
                utime.sleep(0.5)
            if yesButton.value()==1 and level==0: 
                # sets times
                times = fullStart(rtc)
                curTime = times[0]
                dose1 = times[1]
                dose2 = times[2]
                dose3 = times[3]
                rtc.datetime([2022,4,1,4,curTime[0],curTime[1],0,0])
                curHr = rtc.datetime()[5]
                curMin = rtc.datetime()[6]
                print(rtc.datetime(),curHr,curMin)
                
                mode =2
                updateStart(curHr,curMin)
                print('mode',mode)
            elif yesButton.value()==1 and level==1:
                mode =1
                displays.demo()
                print('mode',mode)
        elif mode ==1:
            #if in demo mode
            if testButton.value()==1:
                print('test')
                dispense()
            if noButton.value()==1:
                print('change mode')
                mode = 0
                displays.startMenu1()
                print('mode',mode)
        #if in full mode
        elif mode==2:
            doseCur = (rtc.datetime()[4],rtc.datetime()[5],rtc.datetime()[6])
            if doseCur == dose1 or doseCur == dose2 or doseCur == dose3:
                print(":)")
                dispense()
            if curMin != rtc.datetime()[5]:
                curHr = rtc.datetime()[4]
                curMin = rtc.datetime()[5]
                updateStart(curHr,curMin)
            if yesButton.value()==1:
                mode = 3
                changeSetting(level2)
                print('mode',mode)
        #setting for full
        elif mode == 3:
             if downButton.value()==1:
                level2 += 1
                if level2>1:
                    level2= 0
                changeSetting(level2)
                utime.sleep(0.5)
             if upButton.value()==1:
                level2 -=1
                if level<0:
                    level2=1
                changeSetting(level2)
                utime.sleep(0.5)
            #goes back to mode selction
             if yesButton.value()==1 and level2==1:
                mode = 0
                displays.startMenu1()
                print('mode',mode)
            #changes time values
             elif yesButton.value()==1 and level2==0:
                print('changing time')
                times = fullStart(rtc)
                curTime = times[0]
                dose1 = times[1]
                dose2 = times[2]
                dose3 = times[3]
                rtc.datetime([2022,4,1,4,curTime[0],curTime[1],0,0])
                curHr = rtc.datetime()[5]
                curMin = rtc.datetime()[6]
                print(rtc.datetime(),curHr,curMin)
                mode = 2
                updateStart(curHr,curMin)
                print('mode',mode)
            #goes back to start menu
             if noButton.value()==1:
                mode = 2
                updateStart(curHr,curMin)
                print('mode',mode)
                
    else:
        lcd.backlight_off()
        print([rtc.datetime()[4],rtc.datetime()[5],rtc.datetime()[6]])
        print(dose1)
