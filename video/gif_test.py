import cv2 as cv

fgtersh = 127
capture = cv.VideoCapture("bomb.gif")
fgbg = cv.createBackgroundSubtractorMOG2()
_, frame = capture.read()
video_size = frame.shape
frame_counter = 0
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


while (1):
    ret, frame = capture.read()
    frame_counter += 1
    if frame_counter == 21:
        print("s")
        frame_counter = 0
        capture = cv.VideoCapture("bomb.gif")
    cv.imshow('frame', frame)
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break

capture.release()
cv.destroyAllWindows()
