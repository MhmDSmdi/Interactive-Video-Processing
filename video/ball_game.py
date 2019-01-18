import numpy as np
import cv2 as cv
import random

img_ball = cv.imread("ball.png")
img_ball = cv.resize(img_ball, (20, 20), interpolation=cv.INTER_AREA)

capture = cv.VideoCapture("test.mp4")
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape

balls = []


class Ball:
    speed = 15
    valid = True

    def __init__(self, pos):
        self.pos = pos

    def move(self, dx, dy):
        if dx == 0 and dy == 1:

        elif dx == 0 and dy == -1:

        elif dx == -1 and dy == 0:

        elif dx == 1 and dy == 0: