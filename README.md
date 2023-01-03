# 3D Model Viewer & Interaction Software

### How to use:
    At the moment the engine is only in demo mode, a mode where you can view any 3D file of your choosing is underdevelopment.
    To run the program:
        0. Save the project in its own folder.
        1. Install needed libraries.
        2. In terminal, navigate to the folder and type ```python python3 main.py```
        3. Have fun. Feed back is appreciated!

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


###### NOTE TO SELF
----

###### TO START DO STUFF, START THE VIRTUAL ENVIRONMENT FIRST WTH:
###### source testenv/bin/activate
###### AND THEN RUN YOUR CODE LIKE YOU NORMALLY WOULD!!!!

###### NOTE: YOU ARE USING MEDIAPIPE-SILICON, WHICH IS NOT AN OFFICIAL THING! OR SO I BELIEVE.
###### PYGAME, NUMPY, OPENCV-PYTHON ARE ALL NICE AND REGULAR!!
 
###### This program will allow you to interact with 3D object files with your hands on any computer.
----
