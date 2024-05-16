import serial
import time
from globals import GlobalState
from globals import RobotStats
import serial.tools.list_ports

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            # Try to open and close the port
            # If it fails, it's not the Arduino
            GlobalState().arduino_port = serial.Serial(port.device, 9600, timeout=1)
            time.sleep(3)
            
            
            # If it succeeds, return the port
            return 
        except serial.SerialException:
            pass

    # If no port was found, return None
    return None

#function to be called to set a speed
def command_speed():

    return


# Function to send the integer value to the stepper motor
def send_speed(value):

    
    #port = GlobalState().arduino_port
    port  = GlobalState().arduino_port
    # Convert value to message
    message = "sp" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)
    print("speed "  +str(value) + " sent")

    return


def send_position(value):

    extrusion_speed = RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100

    '''test with constant extrusion'''

    if(value == 0):
        send_speed(0)
    elif(value > 0):
        send_speed(extrusion_speed)
    elif(value < 0):
        send_speed(-extrusion_speed)
    '''end test with constant extrusion'''

    return

    # Convert value to message
    message = "p" + str(value) + ";s" + str(extrusion_speed)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

def retract(direction = -1):

    if direction > 0:
        value = 10
    else:
        value = -10
        
    # Convert value to message
    message = "p" + str(value) + ";s" + str(extrusion_speed)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

    return

def init_steppers():

    find_arduino()
    if GlobalState().arduino_port is None:
        print("Could not find Arduino")

    try: 
        #setup port for arduino communication
        # Configure the serial port
        #GlobalState().arduino_port = serial.Serial('COM27', 9600)  # Replace 'COM3' with the appropriate port 
        #time.sleep(3)

        #initialization sequence
        message = "init"
        message_bytes = message.encode()
        GlobalState().arduino_port.write(message_bytes)
        print("init sent")
    except serial.SerialException:
        print(f"Could not open port {RobotStats().port}")
    
    return

def read_steppers():

    while True:
        #read from serial port
        message = GlobalState().arduino_port.readline()
        print(message)

    return

def wait_ack():
    
    while True:
        print("wait ack")
        try:
            # Read from serial port
            
            message = GlobalState().arduino_port.readline().decode().strip()
            print(message)
            if message == "ack":
                print("acknowledged init")
                break
        except serial.SerialException:
            print("Could not read from port")
            break

    return

def wait_done():
    
    while True:
        print("wait done")
        try:
            # Read from serial port
            
            message = GlobalState().arduino_port.readline().decode().strip()
            print(message)
            if message == "done":
                print("-done init")
                break
        except serial.SerialException:
            print("Could not read from port")
            break

        time.sleep(0.05)
    return

def wait_done_base(theta, index):

    while True:
        print("wait base" + str(theta))
        try:
            # Read from serial port
            message = GlobalState().arduino_port.readline().decode().strip()
            print(message)
            if message == "done:i"+str(index):
                print("base position reached" + str(index))
                break
        except serial.SerialException:
            print("Could not read from port")
            break

    return


def turn_base(theta, index):

    turnspeed_modifier = 1
    #angle = GlobalState().last_base_angle - theta
     #if(angle < 0):
    speed  = GlobalState().printspeed_modifier * turnspeed_modifier
    #else:
    #    speed  = -GlobalState().printspeed_modifier * turnspeed_modifier
    
    speed = speed * 10
    
    port  = GlobalState().arduino_port
    # Convert value to message
    message = "b" + str(theta) + "s" + str(speed)+ "i" + str(index)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)
    print("theta "  +str(theta) + " sent")



    return


def close_steppers():

    # Close the serial port when done
    GlobalState().GlobalState().arduino_portclose()
    
    return
