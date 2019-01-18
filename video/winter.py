import numpy as np
import cv2 as cv
import random

FORGROUND_THRESHOLD = 127

snow_img = cv.imread("snow.png")
snow_img = cv.resize(snow_img, (10, 10), interpolation=cv.INTER_AREA)

cap = cv.VideoCapture('test.mp4')
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = cap.read()
vid_size = frame.shape

snows = []


def paste_image(background, forground, loc):
    for i in range(forground.shape[1]):
        for j in range(forground.shape[0]):
            if not (forground[i][j][2] == 0 and forground[i][j][1] == 0 and forground[i][j][0] == 0):
                try:
                    background[j + loc[0] - 1][i + loc[1] - 1] = forground[j, i]
                except:
                    pass

    return background


class Snow:
    speed = 20
    valid = True

    def __init__(self, position):
        self.position = (0, position)

    def update(self, mask):
        if not self._check_below(mask):
            return
        # print(self.position, self.position[1] + self.speed)
        self.position = (self.position[0] + self.speed, self.position[1])
        if self.position[0] + snow_img.shape[0] > vid_size[0]:
            self.valid = False

    def _check_below(self, mask):
        res = True
        cv.imshow("msk", mask)
        for i in range(self.speed):
            for j in range(snow_img.shape[1]):
                try:

                    if FORGROUND_THRESHOLD < mask[self.position[0] + snow_img.shape[0] + i][self.position[1] + j]:
                        return False

                except:
                    pass
        return True


def generate_snow():
    for i in range(random.choice(range(0, 10))):
        position = random.choice(range(vid_size[1] - snow_img.shape[1]))
        snows.append(Snow(position))


def remove_out_of_bound():
    for snow in snows:
        if not snow.valid:
            snows.remove(snow)


while (1):
    generate_snow()
    remove_out_of_bound()

    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)

    im = frame

    for snow in snows:
        im = paste_image(im, snow_img, snow.position)

    # print(snows)

    # fgmask.resize(100, 100)
    # cv.imshow('frame',fgmask)
    cv.imshow('frame', im)
    # print(im[151][501])
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    for snow in snows:
        snow.update(fgmask)
cap.release()
cv.destroyAllWindows()
