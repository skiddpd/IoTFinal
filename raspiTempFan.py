import requests
import time
import RPi.GPIO as GPIO
import os
import glob


#setup 5V motor
GPIO.setmode(GPIO.BOARD)
int temp = 100

pwma=7
AIN2=11
AIN1=12
STBY=13

# set up GPIO pins for 5v motor
GPIO.setup(pwma, GPIO.OUT) # Connected to PWMA
GPIO.setup(AIN2, GPIO.OUT) # Connected to AIN2
GPIO.setup(AIN1, GPIO.OUT) # Connected to AIN1
GPIO.setup(STBY, GPIO.OUT) # Connected to STBY

#setup temp sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
    if temp>=75:
        # Drive the 5V motor clockwise
        GPIO.output(AIN1, GPIO.HIGH) # Set AIN1
        GPIO.output(AIN2, GPIO.LOW) # Set AIN2
        # Set the motor speed
        GPIO.output(pwma, GPIO.HIGH) # Set PWMA
        # Disable STBY (standby)
        GPIO.output(STBY, GPIO.HIGH)
        # Wait 5 seconds

        #read temp again before restarting loop
        tempc, temp=read_temp()

        #Send a signal to IFTTT
        #eventname = testing
        r = requests.post('https://maker.ifttt.com/trigger/testing/with/key/bd9V2gUrd3UyETgcHA4z42zk0AFCaOevt7NUNAiMtuR',params={"value1":temp,"value2":"none","value3":"none"})
        
        time.sleep(5)

    #check temp of weather
    # Reset all the GPIO pins by setting them to LOW
    if temp <= 75:
        GPIO.output(AIN1, GPIO.LOW) # Set AIN1
        GPIO.output(AIN2, GPIO.LOW) # Set AIN2
        GPIO.output(pwma, GPIO.LOW) # Set PWMA
        GPIO.output(STBY, GPIO.LOW) # Set STBY

        #Read temp again before restarting
        tempc, temp=read_temp()
        #Send a signal to IFTTT
        #eventname = testing
        r = requests.post('https://maker.ifttt.com/trigger/testing/with/key/bd9V2gUrd3UyETgcHA4z42zk0AFCaOevt7NUNAiMtuR',params={"value1":temp,"value2":"none","value3":"none"})
        
        
        time.sleep(5)