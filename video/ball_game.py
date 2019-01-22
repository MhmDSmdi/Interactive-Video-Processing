import cv2 as cv
import time
import math
import random
import datetime

img_ball = cv.imread("assets/ball.png")
img_ball = cv.resize(img_ball, (60, 60), interpolation=cv.INTER_AREA)

img_bomb = cv.imread("assets/bomb.png")
img_bomb = cv.resize(img_bomb, (80, 80), interpolation=cv.INTER_AREA)

capture = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
fourcc = cv.VideoWriter_fourcc(*'MP4V')
out = cv.VideoWriter(
    'out/ball_game_' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H%M%S') + '.mp4', fourcc, 20.0,
    (640, 480))

video_size = frame.shape
fgtersh = 240
is_game_finish = False
total_score = 0
num_lost_ball = 3
items = []


def add_image(background, foreground, loc):
    for j in range(foreground.shape[0]):
        for i in range(foreground.shape[1]):
            if foreground[j][i][2] != 0 and foreground[j][i][1] != 0 and foreground[j][i][0] != 0:
                try:
                    background[j + loc[0]][i + loc[1]] = foreground[j, i]
                except:
                    pass

    return background


def init_items():
    pos = [video_size[0], 382]
    items.append(Ball(1, pos, -2, 1, 0.07, img_ball))


def remove_invalid_items():
    for item in items:
        if not item.valid:
            items.remove(item)


def game_over():
    global is_game_finish, num_lost_ball, total_score
    # is_game_finish = True
    print("Your Score : " + str(total_score))


def generate_item():
    for i in range(random.choice(range(0, 3))):
        bomb_chance = random.choice(range(0, 10))
        xrnd = random.choice(range(0, 7))
        vy = random.choice(range(90, 105)) / -100
        ac = random.choice(range(20, 25)) / 1000
        vx = random.choice(range(-4, 4))
        pos = [video_size[0], xrnd * 80]
        if bomb_chance != 1:
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
            if self.type == 0:
                global num_lost_ball
                num_lost_ball -= 1
                if num_lost_ball == 0:
                    game_over()
        self.time += 1

    def on_item_touched(self):
        pass

    def check_status(self, mask):
        cv.imshow("mask", mask)
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
        self.valid = False
        global total_score
        total_score += 1


class Bomb(AnimatedObject):
    def __init__(self, pos, vy, vx, ac, img):
        super().__init__(pos, vy, vx, ac, img, 1)

    def on_item_touched(self):
        global is_game_finish
        if not is_game_finish:
            game_over()


init_items()
while not is_game_finish:
    remove_invalid_items()
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    if len(items) < 5:
        generate_item()
    im = frame
    for item in items:
        item.throw()
        item.check_status(fgmask)
        im = add_image(im, item.img, item.pos)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, 'SCORE: ' + str(total_score), (10, 40), font, 1, (0, 200, 0), 2,
               cv.LINE_AA)
    cv.putText(frame, 'LOST: ' + str(num_lost_ball), (480, 40), font, 1, (0, 0, 200), 2, cv.LINE_AA)
    cv.imshow('frame', frame)
    out.write(frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break

out.release()
capture.release()
cv.destroyAllWindows()
