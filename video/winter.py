import random
import time

import cv2 as cv

FOREGROUND_THRESHOLD = 127
cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorKNN(0, 2, False)
_, frame = cap.read()
vid_size = frame.shape

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('out/winter' + str(time.time()) + '.avi', fourcc, 20.0, (640, 480))

snow_width = 3
snow_height = 3
snows = []


class Snow:
    speed = 4
    valid = True

    def __init__(self, position):
        self.position = (0, position)

    def update(self, mask):
        if not self._check_below(mask):
            return
        self.position = (self.position[0] + self.speed, self.position[1])
        if self.position[0] + snow_height > vid_size[0]:
            self.valid = False

    def _check_below(self, mask):
        cv.imshow("msk", mask)
        for j in range(snow_width):
            try:
                if FOREGROUND_THRESHOLD < mask[self.position[0] + snow_height][self.position[1] + j]:
                    return False
            except:
                pass
        return True


def generate_snow():
    for i in range(random.choice(range(5, 20))):
        position = random.choice(range(vid_size[1] - 1))
        snows.append(Snow(position))


def draw_snow(pos, background):
    try:
        background[pos[0]][pos[1]] = (255, 255, 255)
        background[pos[0] + 1][pos[1]] = (255, 255, 255)
        background[pos[0] - 1][pos[1]] = (255, 255, 255)
        background[pos[0]][pos[1] + 1] = (255, 255, 255)
        background[pos[0]][pos[1] - 1] = (255, 255, 255)
    except:
        pass

    return background


def remove_out_of_bound():
    for snow in snows:
        if not snow.valid:
            snows.remove(snow)


while 1:
    generate_snow()
    remove_out_of_bound()
    ret, frame = cap.read()
    im = frame
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
    fgmask = cv.GaussianBlur(fgmask, (15, 15), 0)
    ret, thresh = cv.threshold(fgmask, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    for snow in snows:
        im = draw_snow(snow.position, im)
    cv.imshow('frame', im)
    out.write(im)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    for snow in snows:
        snow.update(thresh)
out.release()
cap.release()
cv.destroyAllWindows()
