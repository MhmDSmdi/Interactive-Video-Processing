import numpy as np
import cv2 as cv
import random

img_ball = cv.imread("ball.jpg")
img_ball = cv.resize(img_ball, (50, 50), interpolation=cv.INTER_AREA)
fgtersh = 127
capture = cv.VideoCapture("test.mp4")
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape

balls = []


def paste_image(background, forground, loc):
    for i in range(forground.shape[1]):
        for j in range(forground.shape[0]):
            if not (forground[i][j][2] == 0 and forground[i][j][1] == 0 and forground[i][j][0] == 0):
                try:
                    background[j + loc[0] - 1][i + loc[1] - 1] = forground[j, i]
                except:
                    pass

    return background


class Ball:
    speed = 1
    valid = True

    def __init__(self, pos):
        self.pos = pos

    def _move(self, dx, dy):
        # UP
        if dx == 0 and dy == 1:
            self.pos[0] -= self.speed
        # DOWN
        elif dx == 0 and dy == -1:
            self.pos[0] += self.speed
        # LEFT
        elif dx == -1 and dy == 0:
            self.pos[1] -= self.speed
        # RIGHT
        elif dx == 1 and dy == 0:
            self.pos[1] += self.speed

    def check_status(self, mask):
        for i in range(self.speed):
            for j in range(img_ball.shape[1]):
                cv.imshow("mask", mask)
                print(fgtersh < mask[self.pos[0] + img_ball.shape[0] + i][self.pos[1] + j])
                if fgtersh < mask[self.pos[0] + img_ball.shape[0] + i][self.pos[1] + j]:
                    self._move(0, 1)
                    print("BALL Most GO UP")
                elif fgtersh < mask[self.pos[0] - img_ball.shape[0] + i][self.pos[1] + j]:
                    self._move(0, -1)
                    print("BALL Most GO DOWN")
                elif fgtersh < mask[self.pos[0] + i][self.pos[1] + img_ball.shape[1] + j]:
                    self._move(-1, 0)
                    print("BALL Most GO LEFT")
                elif fgtersh < mask[self.pos[0] + i][self.pos[1] - img_ball.shape[1] + j]:
                    self._move(1, 0)
                    print("BALL Most GO RIGHT")


def init_balls():
    # for i in range(random.choice(range(0, 10))):
    #     print("Ball Append")
    #     pos = random.choice(range(video_size[1] - img_ball.shape[1]))
        pos = [280, 397]
        balls.append(Ball(pos))


def remove_invalid_img():
    for ball in balls:
        if not ball.valid:
            balls.remove(ball)


init_balls()
while (1):
    #remove_invalid_img()
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    im = frame
    for ball in balls:
        im = paste_image(im, img_ball, ball.pos)

    # print(snows)

    # fgmask.resize(100, 100)
    # cv.imshow('frame',fgmask)
    cv.imshow('frame', im)
    # print(im[151][501])
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    for ball in balls:
        ball.check_status(fgmask)
capture.release()
cv.destroyAllWindows()
