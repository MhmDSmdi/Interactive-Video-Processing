import cv2 as cv
import time
import math
import random

fgtersh = 240
img_ball = cv.imread("ball.png")
img_ball = cv.resize(img_ball, (80, 80), interpolation=cv.INTER_AREA)

img_bomb = cv.imread("bomb.png")
img_bomb = cv.resize(img_bomb, (80, 80), interpolation=cv.INTER_AREA)

capture = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape
fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter('ball_game.mp4', fourcc, 20.0, (640, 480))
items = []

total_score = 0
lost_ball = 3


def paste_image(background, forground, loc):
    for i in range(forground.shape[1]):
        for j in range(forground.shape[0]):
            if not (forground[i][j][2] == 0 and forground[i][j][1] == 0 and forground[i][j][0] == 0):
                try:
                    background[j + loc[0] - 1][i + loc[1] - 1] = forground[j, i]
                except:
                    pass

    return background


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
    for i in range(random.choice(range(0, 3))):
        bomb_chance = random.choice(range(0, 2))
        xrnd = random.choice(range(0, 7))
        vy = random.choice(range(90, 115)) / -100
        vx = random.choice(range(0, 2))
        ac = random.choice(range(18, 25)) / 1000
        pos = [video_size[0], xrnd * 80]
        if bomb_chance == 0:
            items.append(Ball(5, pos, vy, vx, ac, img_ball))
        else:
            items.append(Bomb(pos, vy, vx, ac, img_bomb))


class AnimatedObject:
    valid = True
    base_speed = 1
    time = 1

    def __init__(self, pos, vy, vx, ac, img, type=0):
        self.pos = pos
        self.type = type
        self.ac = ac
        self.vy = vy
        self.vx = vx
        self.img = img

    def throw(self):
        v = self.vy + self.ac * self.time
        self.pos[0] += math.ceil(v * self.time)
        self.pos[1] += self.vx
        if self.pos[0] > video_size[0] or self.pos[0] < 0 or self.pos[1] > video_size[1] or self.pos[1] < 0:
            self.valid = False
            global lost_ball
            lost_ball -= 1
        self.time += 1

    def on_item_touched(self):
        pass

    def check_status(self, mask):
        try:
            for i in range(self.img.shape[1]):
                if fgtersh < mask[self.pos[0] + self.img.shape[0]][self.pos[1] + i]:
                    self.on_item_touched()
                if fgtersh < mask[self.pos[0] - self.img.shape[0]][self.pos[1] + i]:
                    self.on_item_touched()
            for j in range(img_ball.shape[0]):
                if fgtersh < mask[self.pos[0] + j][self.pos[1] - self.img.shape[1]]:
                    self.on_item_touched()
                if fgtersh < mask[self.pos[0] + j][self.pos[1] + self.img.shape[1]]:
                    self.on_item_touched()
        except:
            pass


class Ball(AnimatedObject):
    def __init__(self, score, pos, vy, vx, ac, img):
        super().__init__(pos, vy, vx, ac, img, 0)
        self.score = score

    def on_item_touched(self):
        global total_score
        total_score += self.score
        self.valid = False


class Bomb(AnimatedObject):
    def __init__(self, pos, vy, vx, ac, img):
        super().__init__(pos, vy, vx, ac, img, 1)

    def on_item_touched(self):
        print("23wde")
        exit(0)


while 1:
    remove_invalid_items()
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    if len(items) < 5:
        generate_item()
    im = frame
    for item in items:
        item.throw()
        item.check_status(fgmask)
        im = paste_image(im, item.img, item.pos)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, 'SCORE', (87, 100), font, 4, (14, 0, 41), 2, cv.LINE_AA)
    cv.imshow('frame', frame)

    out.write(frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
out.release()
capture.release()
cv.destroyAllWindows()
