import math
import numpy as np

class Projection:
    def __init__(self, env):
        ## Obtaining the "screen" rectangle
        ## (left, top) gives top left point of rectangle.
        ## 

        ## Since distance between camera point and
        ## near clipping plane is always 1 by default.
        RIGHT = math.tan(env.camera.h_fov / 2)
        TOP = math.tan(env.camera.v_fov / 2)
        LEFT = -RIGHT
        BOTTOM = -TOP
        NEAR = env.camera.near_plane
        FAR = env.camera.far_plane

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)

        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        HW = env.H_WIDTH
        HH = env.H_HEIGHT
        ## scales the positions of the verticies of
        ## the object to the scale of the screen. 
        self.screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])




        
        