import cv2 as cv
import time

img_ball = cv.imread("ball.png")
img_ball = cv.resize(img_ball, (80, 80), interpolation=cv.INTER_AREA)
img_bomb = cv.imread("bomb.png")
fgtersh = 127
capture = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape

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

    def __init__(self, pos, v0, ac, imgtype=0):
        self.pos = pos
        self.type = type
        self.ac = ac
        self.v0 = v0

    # def _move(self, dx, dy, coefficient):
    #     # UP
    #     if dx == 0 and dy == 1 and (self.pos[0] - coefficient * self.base_speed) > self.base_speed:
    #         self.pos[0] -= coefficient * self.base_speed
    #     # DOWN
    #     elif dx == 0 and dy == -1 and ((self.pos[0] + self.img.shape[0]) + coefficient * self.base_speed) < video_size[
    #         0] - self.base_speed:
    #         self.pos[0] += coefficient * self.base_speed
    #     # LEFT
    #     elif dx == -1 and dy == 0 and (self.pos[1] - coefficient * self.base_speed) > self.base_speed:
    #         self.pos[1] -= coefficient * self.base_speed
    #     # RIGHT
    #     elif dx == 1 and dy == 0 and ((self.pos[1] + self.img.shape[1]) + coefficient * self.base_speed) < video_size[
    #         1] - self.base_speed:
    #         self.pos[1] += coefficient * self.base_speed
    #
    def throw(self):
        # H = video_size[0] - (v0 ** 2) / (2 * ac)
        # self.pos[0] = video_size[0]
        # while H != h:
        #     # v = v0 - ac
        #     h -= 1
        #     self.pos[0] = h
        # while h != video_size[0]:
        #     h += 1
        #     self.pos[0] = h
        t = 1
        y0 = self.pos[0]
        self.pos[0] = -0.5 * self.ac * (t ** 2) - self.v0 * t + y0
        print(self.pos[0], self.pos[1])
        time.sleep(0.01)
        t += 1


def init_items():
    pos = [video_size[0], 382]
    items.append(AnimatedObject(pos, 1, 1))


init_items()
while (1):
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    im = frame
    for item in items:
        im = paste_image(im, img_ball, item.pos)
    cv.imshow('frame', frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    for item in items:
        item.throw()
capture.release()
cv.destroyAllWindows()
