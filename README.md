# University of Massachusetts Amherst
## Senior Design Project 2024 Team 3 - EZSort
### Evan Raftery, B.S. Computer Engineering
### Jake Shamaly, B.S. Computer Engineering
### Ryan Palmer, B.S. Electrical Engineering

---

Welcome! This repository is the main documentation of our work for ECE415 and ECE416. Our senior design project is EZSort, a modular item sorter that makes use of computer vision and neural networks to classify items. This README file will give a brief overview on what resources were used, how the files function, and how to run the code as a whole.

The JavaScript portion of this code was adapted from the [Teachable Machine Boilerplate](https://github.com/googlecreativelab/teachable-machine-boilerplate/tree/master/dist) GitHub repository. We highly encourage any who are interested in creating lightweight computer vision projects to check out their work, as it is a great starting point.

The main workings of the code are based around the [MobileNet](https://arxiv.org/abs/1704.04861) convolutional neural network (CNN), which was developed by Google specifically for lightweight applications such as webpages or, in our case, applications running with resource limitations. All image processing shown here was run on a Raspberry Pi 4 with 8GB of RAM. Once an image has had its features extracted by MobileNet, we are able to use the [k-nearest neighbors (KNN)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) algorithm which will determine which class the item belongs to.

Our full documentation with all hardware implementations are detailed in the report contained within this repository. In short, we make use of a button to control when we train the object through a USB camera, which will then take our new input images (once training is done) to allow the items present on a custom-built conveyor to be sorted.

## Files
A quick overview of each of the files in this repository and what their purpose is:

- `main.js` Runs all components of image processing and adds images to the KNN training set when training. Transmits data using JSON to main2.py about the current state of training, the most likely class, etc. Can be run as a webpage.

- `main2.py` Handles all GPIO for motor control, receives JSON output from main.js. Runs Flask server for communication with main.js. Handles logic for training and resetting the model.

- `NanoB.ino` Motor control for the conveyor/staging area.

- `NanoS.ino` Motor control for the lazy susan.