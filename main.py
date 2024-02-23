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
    interfacing with the main.js file in order to receive console output and 
    relay the decided class to the motor. This file also contains the dedicated 
    training mode, which allows the user to properly train the model on any 
    number of items (although the lazy susan only supports 4 bins).
    
    For more information on the specifics of computer vision and image processing, 
    see the main.js file in this repository.
"""

from selenium import webdriver
import pyautogui

NUM_CLASSES = 4

def main():
    # Open Chrome to our local page
    driver = webdriver.Chrome()
    driver.get("http://localhost:9966")
    
    # Set up console output to be accessed
    driver.execute_script("""
    console.stdlog = console.log.bind(console);
    console.logs = [];
    console.log = function(){
        console.logs.push(Array.from(arguments));
        console.stdlog.apply(console, arguments);
    }
    """) 
    
    # Training mode, 100 images each class
    train(100)
    
    # Grab the console logs (to be updated with object detection)
    while True:
        logs = driver.execute_script("return console.logs")
        if logs is not None and len(logs) > 0:
            print(logs[-1])

def train(duration):
    for classNum in range(NUM_CLASSES):
        key = str(classNum)
        for i in range(duration):
            pyautogui.keyDown(key)
            pyautogui.keyUp(key)
        pyautogui.keyUp(key)

if __name__ == "__main__":
    main()