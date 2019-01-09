import numpy as np
import math
import cv2



class ImageHandler:
    IMAGE_ADDRESS = "test.jpg"
    VIDEO_ADDRESS = "test.avi"
    image, video = None, None

    def __init__(self):
        self.image = cv2.imread(self.IMAGE_ADDRESS)

    def show_image(self, img=image, title="Image"):
        if img is None:
            cv2.imshow(title, self.image)
        else:
            cv2.imshow(title, img)
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
        self.show_image(rgb_filter, channel + str("_Channel"))

    def show_gray_scale_image(self):
        gray_scale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.show_image(gray_scale_image, "Gray Scale Image")

    def show_gaussian_blur_image(self):
        blur = cv2.GaussianBlur(self.image, (25, 25), 0)
        self.show_image(blur, "Gaussian Smoothing")

    def show_rotation_image(self, angel):
        rows, cols, channels = self.image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angel, 1)
        dst = cv2.warpAffine(self.image, M, (cols, rows))
        self.show_image(dst, str(angel) + " Rotation")

    def show_resize_image(self, width_scale=0.5, height_scale=1):
        resize_image = cv2.resize(self.image, (math.ceil(width_scale * self.image.shape[1]), math.ceil(height_scale * self.image.shape[0])), interpolation=cv2.INTER_LINEAR)
        self.show_image(resize_image, "Image Resize with vector[{}, {}]".format(width_scale, height_scale))

    def show_edges_image(self):
        edges = cv2.Canny(self.image, 100, 200)
        self.show_image(edges, "Edges of Image")

    def show_segmented_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        self.show_image(th3)

    def show_faces_image(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = self.image[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        self.show_image(self.image)

    def get_key(self, prompt):
        return input(prompt)


if __name__ == '__main__':
    imageHandler = ImageHandler()
    imageHandler.show_faces_image()
