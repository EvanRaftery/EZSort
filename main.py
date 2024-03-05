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

# Set up Flask
app = Flask(__name__)
CORS(app)  

global getData
getData = {
    "Train": 1,
    "Clss": -1,
    "Rst": 0
}

def gpioLogic(data):
    categories = ["i0", "i1", "i2", "i3", "i4"]

    highestClass = data['class']
    if highestClass >= 0:
        print(highestClass)
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