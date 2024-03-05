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
BELT = 17
BIT1 = 27
BIT2 = 22

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BELT, GPIO.OUT)  # Whether the belt is allowed to move
GPIO.setup(BIT1, GPIO.OUT)  # Bit 1 of bin
GPIO.setup(BIT2, GPIO.OUT)  # Bit 2 of bin
GPIO.setup(23, GPIO.IN)     # Button

# Initialize Button
BUTTON = Button(23)

global trainClass
trainClass = -1

global iter
iter = 0

global getData
getData = {
    "Train": 1,
    "Clss": -1,
    "Rst": 0
}

def gpioLogic(data):
    if BUTTON.is_pressed:
        if getData["Train"]:
            iter += 1
        else:
            getData["Train"] = 1
    categories = ["i0", "i1", "i2", "i3", "i4"]

    highestClass = data['class']
    if highestClass > 0 and trainClass == -1:
        # print(highestClass)
        
        if highestClass >= 2:
            GPIO.output(BIT1, 1)
        else:
            GPIO.output(BIT1, 0)
        
        if highestClass % 2 == 0:
            GPIO.output(BIT2, 0)
        else:
            GPIO.output(BIT2, 1)
        time.sleep(2)
        
        GPIO.output(BELT, 1)
        time.sleep(2)
        GPIO.output(BELT, 0)

    # GPIO
    """
    1. Long button press sets Rst high
    2. Regular button press for each stage of training
    3. (Option) Only use one button press and after training mode regular press retrains
    """

    # Refresh Page
    """if(data["class"] == 4): # I need to replace this with long button press.(or has js send isRst var)
        getData["Rst"] = 1
        #training = 1
        getData["Train"] = 1
    else:
       getData["Rst"] = 0"""

    # Training Mode
    """
    Train 0 on just belt
    Then train each category on and off to get different angles
    """

    # Below is the working code

    """
    if(getData["Train"]):
        if(getData["Clss"] == -1):
            getData["Clss"] = 0
        if(getData["Clss"] < 5):
            for cat in categories:
                # The below line should be split into increments
                # that only goes off when the button flag is high
                # then sets the button flag low when done.
                # The button flag can be used for LEDs too.
                if data[cat] >= 50 and int(cat[1]) == getData["Clss"]:
                    print(cat, " is over 50: ", data[cat])
                    getData["Clss"] += 1
        else:
            getData["Train"] = 0
            getData["Clss"] = -1
    """

        # trainClass represents the class currently being trained
    
    # getData["Clss"] tells the JS when and what to train 
    # (-1 when waiting for button press so trainClass stores 
    # value for when next iteration of training starts)

    # getData["Train"] is a flag for Python to know when to retrain

    # iter is used for the training iterations

    if(getData["Train"]):

        if(trainClass == -1):
            trainClass = 0
        if(trainClass < 5): 
            for cat in categories:
                if(int(cat[1]) == trainClass):
                    if data[cat] >= (iter*10):
                        getData["Clss"] = -1
                    else:
                       getData["Clss"] = trainClass

                # Might need to move this or change conditional
                if data[cat] >= 50 and int(cat[1]) == getData["Clss"]:
                    print(cat, " is over 50: ", data[cat])
                    trainClass += 1
                    iter = 0
                    #getData["Clss"] += 1
        else:
           getData["Train"] = 0
           trainClass = -1
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