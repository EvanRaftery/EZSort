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
    "Train": 1,
    "Clss": -1,
    "Rst": 0
}

global trainClass
trainClass = -1

global itera
itera = 0


def gpioLogic(data):
    global trainClass
    global itera
    categories = ["i0", "i1", "i2", "i3", "i4"]
    if BUTTON.is_pressed:
        if getData["Train"] and not (itera*10 > data[categories[trainClass]]):
            getData["Rst"] = 0
            itera += 1
            time.sleep(1)
        else:
            getData["Train"] = 1
            getData["Rst"] = 1
            


    highestClass = data['class']
    if highestClass > 0:
        print(highestClass)
       
        if highestClass >= 2:
            GPIO.output(BIT1 , 1)
        else:
            GPIO.output(BIT1 , 0)
           
        if highestClass % 2 == 0:
            GPIO.output(BIT2 , 0)
        else:
            GPIO.output(BIT2 , 1)
        # Use highestClass to move shit


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
    if(getData["Train"]):
        print(itera)
        if(trainClass == -1):
            trainClass = 0
        if(trainClass < 5):
            for cat in categories:
                if(int(cat[1]) == trainClass):
                    if(data[cat] >= (itera*10)):
                        getData["Clss"] = -1
                    else:
                        getData["Clss"] = trainClass
                if data[cat] >= 50 and int(cat[1]) == getData["Clss"]:
                    print(cat, " is over 50: ", data[cat])
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
