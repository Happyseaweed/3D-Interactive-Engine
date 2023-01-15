# 3D Model Viewer & Interaction Software

### Structure:
    main.py         - Contains the engine class for the 3D interactive engine.
    camera.py       - Contains the camera class for the engine.
    projection.py   - Contains the projection class for the engine.
    object.py       - Contains the object class for the engine.
    handModule.py   - Contains a module I made for the MediaPipe hands solution. 
    utility_functions.py
                    - Contains custom transformation functions for matrices.

### How it works:
    It is a 3D engine that utilizes perspective projection(view frustum) to render 3 dimensional objects on a 2D screen.
    The engine allows interaction between user and the environment through **keyboard and mouse** or **their hands and their webcam**. 
    The hand gestures allow for a more intuitive interaction with the objects in the space. 

    Note: There may still be small bugs or weird behaviours, I am still looking for ways to improve the efficiency of OpenCV & MediaPipe and the accuracy of my gesture detections. I might build my own version of MediaPipe if necessary.

#### Libraries Used
    MediaPipe       - For the hand detection. I am using MediaPipe-silicon to work 
                      with my MBP. The silicon build is different from the official build.
    
    OpenCV          - A computer vision library required for hand detection using
                      cameras to work. This is mainly used to take input from webcam and feed input image into hand detection algorithm.

    Pygame          - A python game library that is mainly used for displaying the 
                      2D projection of the environment. Mostly user interface stuff is used.
    
    Numpy           - A library used for matrix multiplications. Used in calculation of
                      transformation & projection matrices, position vectors, orientation vectors, etc...
    
    Math            - Standard Python math library for trignometry functions.


######NOTE TO SELF
----

TO START DO STUFF, START THE VIRTUAL ENVIRONMENT FIRST WTH:
source testenv/bin/activate
AND THEN RUN YOUR CODE LIKE YOU NORMALLY WOULD!!!!

NOTE: YOU ARE USING MEDIAPIPE-SILICON, WHICH IS NOT AN OFFICIAL THING! OR SO I BELIEVE.
PYGAME, NUMPY, OPENCV-PYTHON ARE ALL NICE AND REGULAR!!
 
This program will allow you to interact with 3D object files with your hands on any computer.
----