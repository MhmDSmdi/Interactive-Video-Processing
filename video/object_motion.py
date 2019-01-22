import time

import cv2 as cv

img_ball = cv.imread("assets/ball.png")
img_ball = cv.resize(img_ball, (50, 50), interpolation=cv.INTER_AREA)
fgtersh = 200
capture = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('out/fgbg' + str(time.time()) + '.avi', fourcc, 20.0, (640, 480))

balls = []


def paste_image(background, foreground, loc):
    for i in range(foreground.shape[1]):
        for j in range(foreground.shape[0]):
            if not (foreground[i][j][2] == 0 and foreground[i][j][1] == 0 and foreground[i][j][0] == 0):
                try:
                    background[j + loc[0] - 1][i + loc[1] - 1] = foreground[j, i]
                except:
                    pass

    return background


class Ball:
    valid = True
    base_speed = 1

    def __init__(self, pos):
        self.pos = pos

    def _move(self, dx, dy, coefficient):
        # UP
        if dx == 0 and dy == 1 and (self.pos[0] - coefficient * self.base_speed) > self.base_speed:
            self.pos[0] -= coefficient * self.base_speed
        # DOWN
        elif dx == 0 and dy == -1 and ((self.pos[0] + img_ball.shape[0]) + coefficient * self.base_speed) < video_size[
            0] - self.base_speed:
            self.pos[0] += coefficient * self.base_speed
        # LEFT
        elif dx == -1 and dy == 0 and (self.pos[1] - coefficient * self.base_speed) > self.base_speed:
            self.pos[1] -= coefficient * self.base_speed
        # RIGHT
        elif dx == 1 and dy == 0 and ((self.pos[1] + img_ball.shape[1]) + coefficient * self.base_speed) < video_size[
            1] - self.base_speed:
            self.pos[1] += coefficient * self.base_speed

    def check_status(self, mask):
        # cv.imshow("mask", mask)
        try:
            for i in range(img_ball.shape[1]):
                if fgtersh < mask[self.pos[0] + img_ball.shape[0]][self.pos[1] + i]:
                    coefficient = (mask[self.pos[0] + img_ball.shape[0]][self.pos[1] + i])
                    print(coefficient)
                    self._move(0, 1, 1)
                    # print("BALL Most GO UP")
                if fgtersh < mask[self.pos[0] - img_ball.shape[0]][self.pos[1] + i]:
                    # coefficient = mask[self.pos[0] - img_ball.shape[0]][self.pos[1] + i] / 255
                    self._move(0, -1, 1)
                    # print("BALL Most GO DOWN")

            for j in range(img_ball.shape[0]):
                if fgtersh < mask[self.pos[0] + j][self.pos[1] - img_ball.shape[1]]:
                    # coefficient = mask[self.pos[0] + j][self.pos[1] - img_ball.shape[1]] / 255
                    self._move(1, 0, 1)
                    # print("BALL Most GO RIGHT")

                if fgtersh < mask[self.pos[0] + j][self.pos[1] + img_ball.shape[1]]:
                    # coefficient = mask[self.pos[0] + j][self.pos[1] + img_ball.shape[1]] / 255
                    self._move(-1, 0, 1)
                    # print("BALL Most GO LEFT")

        except:
            pass


def init_balls():
    pos = [280, 397]
    balls.append(Ball(pos))


def remove_invalid_img():
    for ball in balls:
        if not ball.valid:
            balls.remove(ball)


init_balls()
while (1):
    ret, frame = capture.read()
    fgmask = fgbg.apply(frame)
    cv.imshow("main", fgmask)
    fgmask = cv.GaussianBlur(fgmask, (5, 5), 0)
    im = frame
    for ball in balls:
       im = paste_image(im, img_ball, ball.pos)
    cv.imshow('frame', im)
    out.write(frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    for ball in balls:
       ball.check_status(fgmask)
out.release()
capture.release()
cv.destroyAllWindows()
