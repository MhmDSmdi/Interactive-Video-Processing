import numpy as np
import cv2


class ImageHandler:
    IMAGE_ADDRESS = "test.jpg"
    VIDEO_ADDRESS = "test.avi"
    image, video = None, None

    def __init__(self):
        self.image = cv2.imread(self.IMAGE_ADDRESS)
        print(self.image.shape)

    def show_image(self, img=image):
        cv2.imshow('Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_color_channel(self, channel):
        rgb_filter = self.image.copy()
        if channel is 'B':
            rgb_filter[:, :, 1] = 0
            rgb_filter[:, :, 2] = 0

        elif channel is 'R':
            rgb_filter[:, :, 0] = 0
            rgb_filter[:, :, 1] = 0

        elif channel is 'G':
            rgb_filter[:, :, 2] = 0
            rgb_filter[:, :, 0] = 0
        self.show_image(rgb_filter)

    def get_key(prompt):
        return input(prompt)


if __name__ == '__main__':
    imageHandler = ImageHandler()
    imageHandler.show_color_channel('B')
