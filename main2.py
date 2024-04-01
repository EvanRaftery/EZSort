"""
    ####################
    ##### SDP 2024 #####
    ###### TEAM 3 ######
    ##### SDP CODE #####
    ####################

    Team Members:
        Evan Raftery
        Jake Shamaly
        Ryan Palmer
    
    Project Name:
        EZSort
        
    Advisor:
        Prof. Dennis Goeckel
        
    Evaluators:
        Prof. Robert Jackson
        Prof. Nikhil Saxena
        
    This is the primary code file for Team 3's SDP. This file revolves around 
    interfacing with the main.js file in order to receive output and relay the 
    decided class to the motor. This file also contains the dedicated training 
    mode, which allows the user to properly train the model on any number of 
    items (although the lazy susan only supports 4 bins).
    
    The Flask server used to communicate between Python and JS is also set up
    here, allowing for essential data to be passed to make the program run
    smoothly.
    
    For more information on the specifics of computer vision and image processing, 
    see the main.js file in this repository.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import RPi.GPIO as GPIO
from gpiozero import Button
import time

# Set up Flask
app = Flask(__name__)
CORS(app)  

# Defining GPIO pins
BUTTON_PRESS = 23
BELT = 26
BIT1 = 5
BIT2 = 6

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BELT, GPIO.OUT)
GPIO.setup(BIT1, GPIO.OUT)
GPIO.setup(BIT2, GPIO.OUT)
GPIO.setup(23, GPIO.IN)

# Initialize LEDs
BUTTON = Button(23)

# Define data formatting
global getData
getData = {
    "Train": 0,
    "Clss": -1,
    "Rst": 0
}

global trainClass
trainClass = -1

global prevClass
prevClass = -2

global itera
itera = 0

global N
N = 4

global M
M = 16

global waitTime
waitTime = 5

"""
GPIO

1. One button press per set of images - regular button press for each stage of training
2. Must press one more time after training is done to initiate sorting
3. Long press after training is done will reset and restart training
"""
def gpioLogic(data):
    global trainClass
    global itera
    global prevClass
    global N
    global M
    global waitTime
    categories = ["i0", "i1", "i2", "i3"]
    
    # Button control
    if BUTTON.is_pressed:
        GPIO.output(BIT1, 1)
        GPIO.output(BIT2, 0)
        
        if getData["Train"] and not (itera*N > data[categories[trainClass]]):
            itera += 1
            time.sleep(1)
        elif(not getData["Train"] and not data["i3"]):
            getData["Train"] = 1
            getData["Rst"] = 0
        elif(not getData["Train"] and data["i3"] > M-1): # Reset!
            getData["Rst"] = 1
            
    # Read highest class and transmit through GPIO for motor control
    # In decimal, the binary value represented by BIT1 and BIT2 are read like this: 
    # 2*BIT1 + BIT2
    highestClass = data['class']
    if highestClass > 0 and not getData["Train"]:
        GPIO.output(BELT, 0)       
        if highestClass >= 2:
            GPIO.output(BIT1 , 1)
        else:
            GPIO.output(BIT1 , 0)
           
        if highestClass % 2 == 0:
            GPIO.output(BIT2 , 0)
        else:
            GPIO.output(BIT2 , 1)
        if prevClass == highestClass:
            time.sleep(5)
            GPIO.output(BIT1, 0)
            GPIO.output(BIT2, 0)
    if prevClass != -1 and highestClass > 0:
        prevClass = highestClass

    # Training Mode
    """
    Train 0 on just belt
    Then train each category on and off to get different angles
    """
    """
    if(getData["Train"]):
        GPIO.output(BELT, 1)
        #print(itera)
        if(trainClass == -1):
            trainClass = 0
        if(trainClass < 4):
            for cat in categories:
                if(int(cat[1]) == trainClass):
                    if(data[cat] >= (itera*10)):
                        getData["Clss"] = -1
                        GPIO.output(BIT1, 0)
                        GPIO.output(BIT2, 1)
                    else:
                        getData["Clss"] = trainClass
                if data[cat] >= 20 and int(cat[1]) == getData["Clss"]:
                    #print(cat, " is over 50: ", data[cat])
                    trainClass += 1
                    itera = 0
                    #getData["Clss"] += 1
        else:
            getData["Train"] = 0
            trainClass  = -1
            getData["Clss"] = -1
    """
            
    if(getData["Train"]):
        GPIO.output(BELT, 1)
        #print(itera)
        if(trainClass == -1):
            trainClass = 0
        if(trainClass < 4):
            for cat in categories:
                if(int(cat[1]) == trainClass):
                    if(data[cat] >= (itera*N)):
                        getData["Clss"] = -1
                        GPIO.output(BIT1, 0)
                        GPIO.output(BIT2, 0)
                        time.sleep(waitTime)
                        GPIO.output(BIT1, 0)
                        GPIO.output(BIT2, 1)
                        time.sleep(waitTime)
                        GPIO.output(BIT1, 1)
                        GPIO.output(BIT2, 0)
                        time.sleep(waitTime)
                        GPIO.output(BIT1, 1)
                        GPIO.output(BIT2, 1)
                        time.sleep(waitTime)

                    else:
                        getData["Clss"] = trainClass
                if data[cat] >= M and int(cat[1]) == getData["Clss"]:
                    #print(cat, " is over 50: ", data[cat])
                    trainClass += 1
                    itera = 0
                    #getData["Clss"] += 1
        else:
            getData["Train"] = 0
            trainClass  = -1
            getData["Clss"] = -1


# Event handling
@app.route("/", methods=["GET", "POST"])
@cross_origin()
def handle_request():
    if request.method == "POST":
        data = request.get_json(force=True)
        gpioLogic(data)
        return jsonify(data)
    elif request.method == "GET":
        return jsonify(getData)  
    else:
        return "Method not supported", 405


if __name__ == "__main__":
    app.run(debug=True)