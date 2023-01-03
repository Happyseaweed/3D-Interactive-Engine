import math
import numpy as np
import pygame as pg
from utility_functions import *

class Camera:
    def __init__(self, env, position):
        self.env = env

        ## * Camera State, determines whether camera is moving or not.
        ## * 1 = Moving, 0 = Not Moving.
        self.cam_state = 1

        ## * Movement:
        self.movement_speed = 0.20
        self.rotation_speed = 0.020

        ## * Mouse Controls:
        self.both_held = False
        self.mouse_held = False
        self.dist = 0
        self.centerx = 0
        self.centery = 0
        self.mx = 0
        self.my = 0
        self.mx2 = 0
        self.my2 = 0

        ## * Position and orientation vectors.
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        self.pitchAngle = 0
        self.rollAngle  = 0
        self.yawAngle   = 0

        ## View Frustum:
        ##      Horizontal FOV: 60 degrees, π/3 radians.
        ##      Vertical FOV:   Depends on horizontal, preserve h/w ratio. 
        self.h_fov = math.pi / 3    
        self.v_fov = self.h_fov * (env.SCREEN_HEIGHT / env.SCREEN_WIDTH)  
        self.near_plane = 0.1
        self.far_plane = 100

    def control(self):
        keyboard = pg.key.get_pressed()

        ## * Camera State:
        if self.env.DEBUG:
            if self.cam_state == 1:
                print("Camera Rotation")
            else:
                print("Object Rotation")

        ## * Movement:
        if keyboard[pg.K_w]:
            self.position += self.forward * self.movement_speed
        if keyboard[pg.K_s]:
            self.position -= self.forward * self.movement_speed
        if keyboard[pg.K_d]:
            self.position += self.right * self.movement_speed
        if keyboard[pg.K_a]:
            self.position -= self.right * self.movement_speed
        if keyboard[pg.K_e]:
            self.position += self.up * self.movement_speed
        if keyboard[pg.K_q]:
            self.position -= self.up * self.movement_speed
        
        ## * Rotation:
        if keyboard[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
            
        if keyboard[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)

        if keyboard[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)

        if keyboard[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

        ## * Mouse Controls for perspective on CAMERA.
        mouse = pg.mouse.get_pressed()
        cx, cy = pg.mouse.get_pos()
        dx = cx - self.mx
        dy = cy - self.my

        if mouse[0]:
            if self.mouse_held:

                ## * For debugging/visualization purposes.
                pg.draw.circle(self.env.screen, pg.Color('red'), (cx, cy), 3)
                pg.draw.circle(self.env.screen, pg.Color('red'), (self.mx, self.my), 3)

                ## * Update stored mouse position.
                self.mx = cx
                self.my = cy

                ## * and rotate Change in yaw and pitch
                dyaw, dpitch = 0, 0
                ## * normalizing the difference.
                dx /= self.env.SCREEN_WIDTH
                dy /= self.env.SCREEN_HEIGHT

                # * 
                dyaw = 2 * math.atan(dx / -2)
                dpitch = 2 * math.atan(dy / -2)
                
                if self.cam_state == 1:
                    self.camera_yaw(dyaw)
                    self.camera_pitch(dpitch)
                else:
                    self.env.object.rotate_y(dyaw * 2)
                    self.env.object.rotate_x(dpitch * 2)

                #self.camera_yaw(self.rotation_speed * rx * 3)
                #self.camera_pitch(self.rotation_speed * ry * 3)

            else:
                self.mx, self.my = pg.mouse.get_pos()
                self.mouse_held = True
        else:
            self.mouse_held = False
        
    def hands_free_control(self):
        if not self.env.detector.results.multi_hand_landmarks:
            return

        coords = self.env.detector.checkGrabCnt(self.env.cframe)
        cnt = len(coords)
        ##print("Detected: ", cnt)

        if cnt > 0:
            if cnt == 1: 

                cx, cy = coords[0]
                cx *= self.env.SCREEN_WIDTH
                cy *= self.env.SCREEN_HEIGHT
                ## print("Position: ", cx, " ", cy)
                dx = cx - self.mx
                dy = cy - self.my

                if self.mouse_held:
                    self.mx = cx
                    self.my = cy

                    dyaw, dpitch = 0, 0
                    ## * normalizing the difference.
                    dx /= self.env.SCREEN_WIDTH
                    dy /= self.env.SCREEN_HEIGHT

                    # * 
                    dyaw = 2 * math.atan(dx / -2)
                    dpitch = 2 * math.atan(dy / -2)
                    
                    if self.cam_state == 1:
                        self.camera_yaw(dyaw)
                        self.camera_pitch(dpitch)
                    else:
                        self.env.object.rotate_y(dyaw * 3)
                        self.env.object.rotate_x(dpitch * 3)

                else:
                    ##* Mouse now held, record initial position.
                    self.mx, self.my = cx, cy
                    self.mouse_held = True
            else:
                self.mouse_held = False

            if cnt == 2:
                center1 = self.env.detector.palm_center(self.env.cframe)[0]
                center2 = self.env.detector.palm_center(self.env.cframe)[1]
                center = [0.5*(center1[0]+center2[0]), 0.5*(center1[1]+center2[1])]
                dist = self.env.detector.dist(center1[0], center1[1], center2[0], center2[1])

                if self.both_held:
                    ##* Already in the zoom/translate stage.
                    dd = dist - self.dist
                    self.position += self.forward * self.movement_speed * (dd/50)
                    self.dist = dist
                else:
                    self.mx, self.my = center1[0], center1[1]
                    self.mx2, self.my2 = center2[0], center2[1]
                    self.centerx, self.centery = center[0], center[1]
                    self.dist = dist
                    self.both_held = True
            else:
                self.both_held = False
            
        else:
            self.both_held = False
            self.mouse_held = False

    def camera_yaw(self, angle):
        self.yawAngle += angle
    
    def camera_pitch(self, angle):
        self.pitchAngle += angle

    def update_rotation(self):
        rotate = rotate_x(self.pitchAngle) @ rotate_y(self.yawAngle)
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        
        self.forward = self.forward @ rotate
        self.up = self.up @ rotate
        self.right = self.right @ rotate

    def translation_matrix(self):
        # Returns a matrix that allows object to
        # translate objects into camera space.
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]

        ## print(x,y,z)
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotation_matrix(self):
        rx = self.right[0]
        ry = self.right[1]
        rz = self.right[2]

        fx = self.forward[0]
        fy = self.forward[1]
        fz = self.forward[2]

        ux = self.up[0]
        uy = self.up[1]
        uz = self.up[2]

        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        # For convenience. 
        self.update_rotation()
        return self.translation_matrix() @ self.rotation_matrix()