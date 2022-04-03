import machine
import utime
from pico_i2c_lcd import I2cLcd
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)
ex = bytearray([0x00,0x00,0x11,0x0A,0x04,0x0A,0x11,0x00])
lcd.custom_char(3, ex)

def startMenu1():
    lcd.clear()
    lcd.putstr("Full Mode          "+chr(0x7F))
    lcd.putstr("\nDemo Mode  ")
    
def startMenu2():
    lcd.clear()
    lcd.putstr("Full Mode           ")
    lcd.putstr("Demo Mode          "+chr(0x7F))
    
def demo():
    lcd.clear()
    lcd.putstr("10:00               ")
    lcd.putstr("\nNext Dose:"+"10:30     ")
    lcd.putstr("(Press button on    back to dispense)")
    
def pillOut():
    lcd.clear()
    lcd.putstr("A dose has been     dispensed           ")
    lcd.putstr("Please take the     medication")
    
def thanks():
    lcd.clear()
    lcd.putstr("Thank you for taking the medication")
    
def startMenu(hr,curMin,nextDose):
    lcd.clear()
    lcd.putstr(str(hr)+":"+str(curMin))
    lcd.putstr("               Next Dose:"+nextDose)
    lcd.putstr("                         Settings"+"           "+chr(0x7F))
 

def settingMenu1():
    lcd.clear()
    lcd.putstr("change times       "+chr(0x7F))
    lcd.putstr("change mode")
    lcd.putstr('                             cancel             '+chr(3))
 
    
def settingMenu2():
    lcd.clear()
    lcd.putstr("change times        ")
    lcd.putstr("change mode        "+chr(0x7F))
    lcd.putstr('                    cancel             '+chr(3))
    


    
    

