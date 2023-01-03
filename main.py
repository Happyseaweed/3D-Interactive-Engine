import cv2 as cv
import mediapipe as mp
import pygame as pg
import numpy as np
import math

from object import *
from camera import Camera
from projection import Projection
import handModule as hm

print("Hello World")


################################################################################
################################################################################



################################################################################
################################################################################

class Engine:
    def __init__(self, debug = False, w = 1366, h = 768, bgcolor = (46, 52, 64), fps = 60):
        pg.init()
        ## * 1: Keyboard & Mouse, 0: Hands Free (Mostly) Mode
        self.STATE = 0
        self.RUNNING = True

        ## * OpenCV & Hand Detector Module
        self.cap = cv.VideoCapture(0)
        self.detector = hm.HandDetector(detectionCon=0.50, trackCon=0.50)
        self.cframe = 0
        self.hasHands = False

        ## * Regular Engine Stuff.
        self.DEBUG = debug
        self.SCREEN_WIDTH = w
        self.SCREEN_HEIGHT= h
        self.H_WIDTH = self.SCREEN_WIDTH // 2
        self.H_HEIGHT= self.SCREEN_HEIGHT // 2
        self.FPS = fps
        self.bgcolor = bgcolor
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.clock = pg.time.Clock()
        
        self.init_obj()
        
    def init_obj(self):
        ## Create camera and objects. 
        self.camera = Camera(self, [0, 0, -5])
        self.projection = Projection(self)
        self.object = Object(self)

        ## Debugging purposes
        self.object.translate([-0.5, -0.5, -0.5])
        self.object.rotate_y(math.pi / 6)
        self.axes = Axes(self)

    def draw(self):
        self.screen.fill(self.bgcolor)
        self.object.draw()
        self.axes.draw()

    def run(self, debug = False):

        while self.RUNNING:
            self.draw()
            
            ## * OpenCV Processing:
            _, self.cframe = self.cap.read()
            self.cframe = cv.flip(self.cframe, 1)
            self.cframe.flags.writeable = False
            img = self.detector.findHands(self.cframe)
            self.detector.findPosition(self.cframe, 2)
            self.hasHands = self.detector.results.multi_hand_landmarks

            ## * Pygame User Interface
            font = pg.font.SysFont('Comic Sans MS', 20)
            ## Control state:
            mode_string = ""
            if self.STATE == 1:
                mode_string = "Keyboard & Mouse"
            else:
                mode_string = "Hands Free"
            
            state_display_surface = font.render("Control Mode: " + mode_string, False, (129, 161, 193))
            self.screen.blit(state_display_surface, (32, 20))
            
            ## Viewing State:
            views_string = ""
            if self.camera.cam_state == 1:
                views_string = "Free Movement"
            else:
                views_string = "Object Locked"
            
            views_display_surface = font.render("Viewing Mode: " + views_string, False, (129, 161, 193))
            self.screen.blit(views_display_surface, (32, 50))

            instr1_display_surface = font.render("[WASDQE] + [Left Click]", False, (129, 161, 193))
            instr2_display_surface = font.render("[Grab With Hand & Drag]", False, (129, 161, 193))
            instr3_display_surface = font.render("[M]: Change Control Mode   [P]: Change View Mode", False, (129, 161, 193))
            self.screen.blit(instr1_display_surface, (32, 650))
            self.screen.blit(instr2_display_surface, (32, 680))
            self.screen.blit(instr3_display_surface, (32, 710))

            ## * Engine States for K&M vs HFC
            if self.STATE == 1:
                self.camera.control()
            else:
                self.camera.hands_free_control()

            ## * ---------- Events:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()

                ##! Absolute brilliance :D
                if event.type == pg.KEYUP:
                    if event.key == pg.K_p:
                        self.camera.cam_state ^= 1
                    if event.key == pg.K_m:
                        self.STATE ^= 1

            # Meat & Potatoes:
            pg.display.set_caption("FPS:" + str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

        self.cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    engine1 = Engine(False)
    engine1.run()
    




    



