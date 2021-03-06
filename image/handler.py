import math

import cv2
import numpy as np


class ImageHandler:
    IMAGE_ADDRESS = "image.png"
    VIDEO_ADDRESS = "test.mp4"
    image, video = None, None

    def __init__(self):
        self.image = cv2.imread(self.IMAGE_ADDRESS)
        self.image = cv2.resize(self.image, (500, 600), interpolation=cv2.INTER_LINEAR)

    # a
    def show_image(self, img=image, title="Image"):
        if img is None:
            cv2.imshow(title, self.image)
        else:
            cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # b
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

    # c
    def show_gray_scale_image(self):
        gray_scale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.show_image(gray_scale_image, "Gray Scale Image")

    # d
    def show_gaussian_blur_image(self):
        blur = cv2.GaussianBlur(self.image, (25, 25), 0)
        self.show_image(blur, "Gaussian Smoothing")

    # e
    def show_rotation_image(self, angel):
        rows, cols, channels = self.image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angel, 1)
        dst = cv2.warpAffine(self.image, M, (cols, rows))
        self.show_image(dst, str(angel) + " Rotation")

    # f
    def show_resize_image(self, width_scale=0.5, height_scale=1):
        resize_image = cv2.resize(self.image, (
            math.ceil(width_scale * self.image.shape[1]), math.ceil(height_scale * self.image.shape[0])),
                                  interpolation=cv2.INTER_LINEAR)
        self.show_image(resize_image, "Image Resize with vector[{}, {}]".format(width_scale, height_scale))

    # g
    def show_edges_image(self):
        edges = cv2.Canny(self.image, 100, 200)
        self.show_image(edges, "Edges of Image")

    # h
    def show_segmented_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(self.image, markers)
        self.image[markers == -1] = [255, 0, 0]
        self.show_image(self.image)

    # i
    def show_faces_image(self):
        face_cascade = cv2.CascadeClassifier(
            '/home/mhmd/anaconda3/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        im = self.image
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        self.show_image(im)

    # j
    def show_frame(self, num):
        cap = cv2.VideoCapture(self.VIDEO_ADDRESS)
        for i in range(num):
            _, frame = cap.read()
            frame = cv2.resize(frame, (600, 600), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Frame " + str(i + 1), frame)
            cv2.waitKey(500)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cap.release()

    def get_input(self, key):
        if key == 'a':
            self.show_image(self.image, "Show Image")
        elif key == 'b':
            self.show_color_channel('B')
        elif key == 'c':
            self.show_gray_scale_image()
        elif key == 'd':
            self.show_gaussian_blur_image()
        elif key == 'e':
            self.show_rotation_image(90)
        elif key == 'f':
            self.show_resize_image(0.7, 2)
        elif key == 'g':
            self.show_edges_image()
        elif key == 'h':
            self.show_segmented_image()
        elif key == 'i':
            self.show_faces_image()
        elif key == 'j':
            self.show_frame(5)


if __name__ == '__main__':
    image_handler = ImageHandler()
    # while 1:
    k = input("Enter a - j  -->")
    image_handler.get_input(k)
