import numpy as np
import pygame as pg
from utility_functions import *


## Obejects class.
## __init__:
##          Parameters: self - For accessing self functions
##                      env  - For accessing other objects in the environment.

class Object:
    def __init__(self, env):
        self.env = env
        self.axes = False
        self.vertices = np.array([
            (0, 0, 0, 1), # 0: Front bottom left
            (0, 0, 1, 1), # 1: Back bottom left
            (0, 1, 0, 1), # 2: Front top left
            (0, 1, 1, 1), # 3: Back top left
            (1, 0, 0, 1), # 4: Front bottom right
            (1, 1, 0, 1), # 5: Front top right
            (1, 1, 1, 1), # 6: Back top right
            (1, 0, 1, 1)  # 7: Back bottom right.
        ])

        self.faces = np.array([
            (0, 1, 3, 2), # Left face
            (0, 4, 5, 2), # Front face
            (4, 5, 6, 7), # Right face
            (2, 5, 6, 3), # Top face
            (0, 1, 7, 4), # Bottom face
            (1, 3, 6, 7), # Back face.
        ])

        self.color_faces = [
            (pg.Color("white"), face) for face in self.faces
        ]

        print("Object Initialized!")

    def draw(self):
        self.object_projection()

    def object_projection(self):
        ## First transform object coordinates into camera space.
        ## translation & rotation matrix from camera.
        ## !! Don't change the original vertices np array
        vertices = self.vertices @ self.env.camera.camera_matrix()
        vertices = vertices @ self.env.projection.projection_matrix
        
        ## Divide by w and zero the values beyond 1, -1.
        vertices /= vertices[:, -1].reshape(-1, 1)
        ## Setting values greater than 2 to 0, 2 because we 
        ## want to get some what close to the vertices without
        ## the faces disappearing.
        #vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.env.projection.screen_matrix
        vertices = vertices[:, :2]

        ## Drawing:
        for face in self.color_faces:
            color, surface = face
            surface = vertices[surface]
            if not np.any((surface == self.env.H_WIDTH) | (surface == self.env.H_HEIGHT)):
                pg.draw.polygon(self.env.screen, color, surface, 2)
        
        for ind, vertex in enumerate(vertices):
            ## print(ind," ", vertex)
            if not np.any((vertex == self.env.H_WIDTH) | (vertex == self.env.H_HEIGHT)):
                pg.draw.circle(self.env.screen, pg.Color('white'), vertex, 4)
        

    def translate(self, pos):
        # Can use @ for matrix multiplication.
        self.vertices = self.vertices @ translate(pos)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

    def scale(self, toscale):
        self.vertices = self.vertices @ scale(toscale)
    

## Axes object.
class Axes(Object):
    def __init__(self, env):
        super().__init__(env)
        self.axes = True
        self.vertices = np.array([
            (0, 0, 0, 1),
            (0, 2, 0, 1),
            (2, 0, 0, 1),
            (0, 0, 2, 1)
        ])
        self.faces = np.array([
            (0, 1),
            (0, 2),
            (0, 3)
        ])
        self.color_faces = [
            (pg.Color("red"), face) for face in self.faces
        ]


