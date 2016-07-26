import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def find_contour_of_image(name='./images/train/0.jpeg'):
    img = cv2.imread(name, 0)

    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    id = 0
    for i in range(len(contours)):
        if (len(contours[i]) > len(contours[id])):
            id = i

    if (len(contours) > 0):
        img2 = np.zeros((img2.shape[0], img2.shape[1]))
        cv2.drawContours(img2, contours[id], -1, color=255)
    else:
        cv2.drawContours(img2, contours, -1, color=255)
    #plt.subplot(133), plt.imshow(img2, 'gray'), plt.title('contour')
    #plt.show()

    return img2

def find_contour(url='./images/train', features=100):
    file_list = os.listdir(url)
    input = np.empty([len(file_list), features], dtype=np.uint8)
    target = np.empty([len(file_list), 1], dtype=np.uint8)

    for i in range(len(file_list)):
        img2 = find_contour_of_image(url + '\/' + file_list[i])
        kind = file_list[i][-6]

        input[i, :] = img2.ravel()
        target[i] = int(kind)

    return (input, target)
