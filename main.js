/*
    ####################
    ##### SDP 2024 #####
    ###### TEAM 3 ######
    ##### CDR CODE #####
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
        
    This is the image processing and webpage setup code for Team 3's SDP. This file
    first sets up a webpage to display info to the user regarding their model, and
    then lets the user input data to train on. The model makes use of a KNN classifier
    and MobileNet to accurately predict an object's class with minimal training.
*/

import "@babel/polyfill";
import * as mobilenetModule from '@tensorflow-models/mobilenet';        // Our CNN
import * as tf from '@tensorflow/tfjs';
import * as knnClassifier from '@tensorflow-models/knn-classifier';     // Our Classifier

// Number of classes
const NUM_CLASSES = 5;
// Webcam Image size (Recommended is 227)
const IMAGE_SIZE = 227;
// K value for KNN (Number of nearest neighbors to consider)
const TOPK = 10;
// Max delay until object detected
const MAX_COUNT_DELAY = 50;

// Variables for object detection
let prevClass = -1;
let maxCount = 0;


class Main {
    constructor() {
        // Initiate variables
        this.infoTexts = [];
        this.training = -1;         // -1 when no class is being trained
        this.videoPlaying = false;

        // Communication with Python
        this.pydataT = 0;           // 0 or 1, determines if we're training or not
        this.pydataR = 0;           // 0 or 1, tells us when to reset/retrain
        this.maxClass = -1;

        // Initiate deeplearn.js math and knn classifier objects
        this.bindPage();

        // Create video element that will contain the webcam image
        this.video = document.createElement('video');

        // Show webcam (optional)
        // document.body.appendChild(this.video);
        
        // Create training buttons and info texts    
        for (let i = 0; i < NUM_CLASSES; i++) {
            const div = document.createElement('div');
            document.body.appendChild(div);
            div.style.marginBottom = '10px';
            
            // Train class N if number key N is pressed
            // document.addEventListener('keypress', (event) => {if(event.key === String(i)){this.training = i;}});
            // document.addEventListener('keyup', (event) => {if(event.key === String(i)){this.training = -1;}});
            
            // Create info text
            const infoText = document.createElement('span')
            infoText.innerText = " No examples added";
            div.appendChild(infoText);
            this.infoTexts.push(infoText);
        }


        // Setup webcam
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then((stream) => {
            this.video.srcObject = stream;
            this.video.width = IMAGE_SIZE;
            this.video.height = IMAGE_SIZE;

            this.video.addEventListener('playing', () => this.videoPlaying = true);
            this.video.addEventListener('paused', () => this.videoPlaying = false);
        })
    }

    async bindPage() {
        this.knn = knnClassifier.create();
        this.mobilenet = await mobilenetModule.load();

        this.start();
    }

    start() {
        if (this.timer) {
            this.stop();
        }
        this.video.play();
        this.timer = requestAnimationFrame(this.animate.bind(this));
    }

    stop() {
        this.video.pause();
        cancelAnimationFrame(this.timer);
    }

    // Recieve communication from Python
    async recieve() {
        let thing = await fetch('http://127.0.0.1:5000/');
        let things = await thing.json();
        this.pydataT = things.Train;
        this.training = things.Clss;
        this.pydataR = things.Rst;
        return(things);
    }

    // Send classifcation info to Python
    send(clss, c0, c1, c2, c3, c4) {
        // Account for case where a class has no training data
        if(!c0){c0 = 0;}
        if(!c1){c1 = 0;}
        if(!c2){c2 = 0;}
        if(!c3){c3 = 0;}
        if(!c4){c4 = 0;}

        // Set up json data to be sent
        const data = {
            i0: c0,
            i1: c1,
            i2: c2,
            i3: c3,
            i4: c4,
            class: clss
        };

        fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(responseData => {
            //console.log('Data sent successfully:', responseData);
        })
        .catch(error => {
            console.error('Error sending data:', error);
        });
    }

    //logic(){
        // start here
    //}

    async animate() {
        this.recieve();
        // this.logic();      // Only going to remove if we do not need anymore logic.

        if (this.videoPlaying) {
            // Get image data from video element
            const image = tf.fromPixels(this.video);

            let logits;
            // 'conv_preds' is the logits activation of MobileNet.
            const infer = () => this.mobilenet.infer(image, 'conv_preds');

            // Train class if one of the buttons is held down
            if (this.training != -1) {
                logits = infer();

                // Add current image to classifier
                this.knn.addExample(logits, this.training)
            }

            const numClasses = this.knn.getNumClasses();
            if (numClasses > 0) {

                let max = 0;
                this.maxClass = "None";
                let sendClass = 0;
                // If classes have been added run predict
                logits = infer();
                const res = await this.knn.predictClass(logits, TOPK);

                for (let i = 0; i < NUM_CLASSES; i++) {
                    // The number of examples for each class
                    const exampleCount = this.knn.getClassExampleCount();

                    // Update info text
                    if (exampleCount[i] > 0) {
                        this.infoTexts[i].innerText = ` ${exampleCount[i]} examples - ${res.confidences[i] * 100}%`
                        if(res.confidences[i] > max) {
                            max = res.confidences[i];
                            this.maxClass = i;
                        }
                    }
                }
                if (this.maxClass == prevClass) {    // Same class we've been looking at
                    maxCount = maxCount + 1;
                } else {                        // New item detected!
                    maxCount = 1;
                    prevClass = this.maxClass;
                }
                /*if (maxCount > MAX_COUNT_DELAY && maxCount % 25 == 0) {
                this.send(maxClass,this.knn.getClassExampleCount()[0],this.knn.getClassExampleCount()[1], this.knn.getClassExampleCount()[2], this.knn.getClassExampleCount()[3], this.knn.getClassExampleCount()[4]);
                console.log(maxClass, maxCount); 
                }else{
                this.send("None",this.knn.getClassExampleCount()[0],this.knn.getClassExampleCount()[1], this.knn.getClassExampleCount()[2], this.knn.getClassExampleCount()[3], this.knn.getClassExampleCount()[4]);
                }*/
            }

            if (maxCount > MAX_COUNT_DELAY && maxCount % 25 == 0) {
                this.send(this.maxClass,this.knn.getClassExampleCount()[0],this.knn.getClassExampleCount()[1], this.knn.getClassExampleCount()[2], this.knn.getClassExampleCount()[3], this.knn.getClassExampleCount()[4]);
                console.log(this.maxClass, maxCount); 
            }else{
                this.send(-1,this.knn.getClassExampleCount()[0],this.knn.getClassExampleCount()[1], this.knn.getClassExampleCount()[2], this.knn.getClassExampleCount()[3], this.knn.getClassExampleCount()[4]);
            }

            // Dispose image when done
            image.dispose();
            if (logits != null) {
                logits.dispose();
            }
        }
        this.timer = requestAnimationFrame(this.animate.bind(this));
    }
}


window.addEventListener('load', () => new Main());