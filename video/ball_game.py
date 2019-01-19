import cv2 as cv
import time
import math
import random

img_ball = cv.imread("ball.png")
img_ball = cv.resize(img_ball, (80, 80), interpolation=cv.INTER_AREA)
img_bomb = cv.imread("bomb.png")
fgtersh = 127
capture = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape
print(video_size)
items = []


def paste_image(background, forground, loc):
    for i in range(forground.shape[1]):
        for j in range(forground.shape[0]):
            if not (forground[i][j][2] == 0 and forground[i][j][1] == 0 and forground[i][j][0] == 0):
                try:
                    background[j + loc[0] - 1][i + loc[1] - 1] = forground[j, i]
                except:
                    pass

    return background


class AnimatedObject:
    valid = True
    base_speed = 1

    def __init__(self, pos, vy, vx, ac, imgtype=0):
        self.pos = pos
        self.type = type
        self.ac = ac
        self.vy = vy
        self.vx = vx

    def throw(self, t):
        v = self.vy + self.ac * t
        self.pos[0] += math.ceil(v * t)
        self.pos[1] += self.vx
        if self.pos[0] > video_size[0] or self.pos[0] < 0 or self.pos[1] > video_size[1] or self.pos[1] < 0:
            self.valid = False

    def check_status(self, mask):
        try:
            for i in range(img_ball.shape[1]):
                if fgtersh < mask[self.pos[0] + img_ball.shape[0]][self.pos[1] + i]:
                    self.valid = False
                if fgtersh < mask[self.pos[0] - img_ball.shape[0]][self.pos[1] + i]:
                    self.valid = False
            for j in range(img_ball.shape[0]):
                if fgtersh < mask[self.pos[0] + j][self.pos[1] - img_ball.shape[1]]:
                    self.valid = False
                if fgtersh < mask[self.pos[0] + j][self.pos[1] + img_ball.shape[1]]:
                    self.valid = False
        except:
            pass


def init_items():
    pos = [video_size[0], 382]
    items.append(AnimatedObject(pos, vy=-1, vx=1, ac=0.025))
    pos = [video_size[0], 100]
    items.append(AnimatedObject(pos, vy=-1.15, vx=1, ac=0.025))
    pos = [video_size[0], 250]
    items.append(AnimatedObject(pos, vy=-1.18, vx=2, ac=0.025))
    pos = [video_size[0], 290]
    items.append(AnimatedObject(pos, vy=-0.95, vx=2, ac=0.025))


def remove_invalid_items():
    for item in items:
        if not item.valid:
            items.remove(item)


def generate_item():
    # rnd = random.choice(range(0, 2))
    # if rnd = 1:
    #
    # else:
    for i in range(random.choice(range(0, 5))):
        xrnd = random.choice(range(0, 7))
        pos = [video_size[0], xrnd * 80]
        items.append(AnimatedObject(pos, vy=-1.15, vx=2, ac=0.025))


#init_items()
t = 1
while 1:
    remove_invalid_items()
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    print(len(items))
    if len(items) < 10:
        generate_item()
    im = frame
    for item in items:
        item.throw(t)
        item.check_status(fgmask)
        im = paste_image(im, img_ball, item.pos)
    cv.imshow('frame', frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    t += 1
capture.release()
cv.destroyAllWindows()
