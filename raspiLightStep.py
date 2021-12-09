import digitalio
import board
import time
import requests

int light = 100

#set up the light sensor
GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit fr light sensor
pin_to_circuit = 7

int set=0

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count


# set up pins for stepper motor
enable_pin = digitalio.DigitalInOut(board.D18)
coil_A_1_pin = digitalio.DigitalInOut(board.D4)
coil_A_2_pin = digitalio.DigitalInOut(board.D17)
coil_B_1_pin = digitalio.DigitalInOut(board.D23)
coil_B_2_pin = digitalio.DigitalInOut(board.D24)

enable_pin.direction = digitalio.Direction.OUTPUT
coil_A_1_pin.direction = digitalio.Direction.OUTPUT
coil_A_2_pin.direction = digitalio.Direction.OUTPUT
coil_B_1_pin.direction = digitalio.Direction.OUTPUT
coil_B_2_pin.direction = digitalio.Direction.OUTPUT

enable_pin.value = True


#allow motor to move forward
def forward(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        i += 1


#allow motor to move backward
def backwards(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        i += 1

#setup the step pins
def setStep(w1, w2, w3, w4):
    coil_A_1_pin.value = w1
    coil_A_2_pin.value = w2
    coil_B_1_pin.value = w3
    coil_B_2_pin.value = w4


while True:

    if light<=101 and set ==0:
        #open the blinds
        forward(0.005, 1000)
        light = rc_time(pin_to_circuit)
        #Send a signal to IFTTT
        #eventname = testing
        r = requests.post('https://maker.ifttt.com/trigger/testing/with/key/bd9V2gUrd3UyETgcHA4z42zk0AFCaOevt7NUNAiMtuR',params={"value1":temp,"value2":"none","value3":"none"})
        time.sleep(5)
        if set == 0:
            set=1

        
    if light>=100 and set ==0:
        #close the blinds
        backwards(0.005, 1000)
        light = rc_time(pin_to_circuit)
        #Send a signal to IFTTT
        #eventname = testing
        r = requests.post('https://maker.ifttt.com/trigger/testing/with/key/bd9V2gUrd3UyETgcHA4z42zk0AFCaOevt7NUNAiMtuR',params={"value1":temp,"value2":"none","value3":"none"})
        time.sleep(5)
        if set == 1:
            set=0