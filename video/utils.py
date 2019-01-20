import cv2
import imageio


def transparency(file_name, output_name):
    src = cv2.imread(file_name, 1)
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    cv2.imwrite(output_name, dst)


def show_gif(file_name):
    gif = imageio.mimread(file_name)
    nums = len(gif)

    # convert form RGB to BGR
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    i = 0
    while True:
        cv2.imshow("gif", imgs[i])
        if cv2.waitKey(100) & 0xFF == 27:
            break
        i = (i + 1) % nums
    cv2.destroyAllWindows()


def proper_image(image):
    for j in range(image.shape[0]):
        for i in range(image.shape[1]):
            if image[j][i][2] != 0 and image[j][i][1] != 0 and image[j][i][0] != 0:
                proper_image('')
    return image
