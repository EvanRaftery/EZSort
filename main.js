
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
import * as mobilenetModule from '@tensorflow-models/mobilenet';      // Our CNN
import * as tf from '@tensorflow/tfjs';
import * as knnClassifier from '@tensorflow-models/knn-classifier';   // Our classifier

// Number of classes
const NUM_CLASSES = 4;
// Webcam Image size. (Default is 227)
const IMAGE_SIZE = 500;
// K value for KNN (number of nearest neighbors to consider)
const TOPK = 10;
// Max delay until object detected
const MAX_COUNT_DELAY = 50;

// Variables for output logging
let prevClass = -1;
let maxCount = 0;


class Main {
  constructor() {
    // Initiate variables
    this.infoTexts = [];
    this.training = -1; // -1 when no class is being trained
    this.videoPlaying = false;

    // Initiate deeplearn.js math and knn classifier objects
    this.bindPage();

    // Create video element that will contain the webcam image
    this.video = document.createElement('video');
    this.video.setAttribute('autoplay', '');
    this.video.setAttribute('playsinline', '');

    // Add video element to DOM
    //document.body.appendChild(this.video);

    // Create training buttons and info texts
    for (let i = 0; i < NUM_CLASSES; i++) {
      const div = document.createElement('div');
      document.body.appendChild(div);
      div.style.marginBottom = '10px';

      // Create training button
      //const button = document.createElement('button')
      //button.innerText = "Train " + i;
      //div.appendChild(button);

      // Listen for mouse events when clicking the button
      //button.addEventListener('mousedown', () => this.training = i);
      //button.addEventListener('mouseup', () => this.training = -1);

      // Listen for key presses for training
      document.addEventListener('keypress', (event) => {if(event.key === String(i)){this.training = i;}});
      document.addEventListener('keyup', (event) => {if(event.key === String(i)){this.training = -1;}});
      
      // Create info text
      const infoText = document.createElement('span')
      infoText.innerText = "No examples added";
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

  async animate() {
    if (this.videoPlaying) {
      // Get image data from the camera
      const image = tf.fromPixels(this.video);

      let logits;
      // 'conv_preds' is the logits activation of MobileNet.
      const infer = () => this.mobilenet.infer(image, 'conv_preds');

      // Train class if one of the buttons/keys is held down
      if (this.training != -1) {
        logits = infer();

        // Add current image to classifier
        this.knn.addExample(logits, this.training)
      }

      const numClasses = this.knn.getNumClasses();

      // Only run KNN classifier if we have added samples to the model
      if (numClasses > 0) {
        // Initialize variables for object detection
        let max = 0;
        let maxClass = "None";

        // Run prediction
        logits = infer();
        const res = await this.knn.predictClass(logits, TOPK);

        for (let i = 0; i < NUM_CLASSES; i++) {
          // The number of examples for each class
          const exampleCount = this.knn.getClassExampleCount();

          // Make the predicted class bold
          if (res.classIndex == i) {
            this.infoTexts[i].style.fontWeight = 'bold';
          } else {
            this.infoTexts[i].style.fontWeight = 'normal';
          }

          // Update info text
          if (exampleCount[i] > 0) {
            this.infoTexts[i].innerText = ` ${exampleCount[i]} examples - ${res.confidences[i] * 100}%`

            // Make note of predictions
            if (res.confidences[i] > max) {
              max = res.confidences[i];
              maxClass = i;
            }
          }
        }

        // Make note of each prediction and how long that predicted class has been predicted for
        if (maxClass == prevClass) {    // Same class we've been looking at
          maxCount = maxCount + 1;
        } else {                        // New item detected!
          maxCount = 1;
          prevClass = maxClass;
        }
        console.log(maxClass, maxCount);    // This console log can be accessed by main.py for motor control
      }

      // Dispose image when done (saves resources)
      image.dispose();
      if (logits != null) {
        logits.dispose();
      }
    }
    this.timer = requestAnimationFrame(this.animate.bind(this));
  }
}

window.addEventListener('load', () => new Main());