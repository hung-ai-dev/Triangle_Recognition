import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import csv

def GenSet(type, n_of_case, triangle_size, height, width):
    triangle = n_of_case * triangle_size
    url = "./images/" + type

    if not os.path.exists(url):
        os.makedirs(url)

    for i in range(n_of_case):
        img = np.zeros((height, width), np.uint8)
        img[:, :] = 255
        if (i < triangle):
            n = 3
            kind = 1 # triangle
        else:
            n = np.random.random_integers(4, 10)
            kind = 0 # other
        pts = []
        for j in range(n):
            x = np.random.random_integers(0, height - 1)
            y = np.random.random_integers(0, width - 1)
            pts.append((x, y))

        cv2.fillPoly(img, [np.array([pts])], 0)
        #Display the image
        #cv2.imshow("img", img)
        #cv2.waitKey(0)

        # 1 for triangle, 0 for other
        cv2.imwrite(url + "/%i_%i.jpeg" % (i, kind), img)

def Convert2Csv(type, n_of_case, triangle_size, height, width):
    image_url = "./images/" + type
    file_list = os.listdir(image_url)
    csv_url = "./csv/"
    if not os.path.exists(csv_url):
        os.makedirs(csv_url)
    file_name = csv_url + type + '.csv'
    triangle = n_of_case * triangle_size

    with open(file_name, 'w', newline='') as mycsvfile:
        target = csv.writer(mycsvfile)

        for i in range(len(file_list)):
            image = cv2.imread(image_url + "\/" + file_list[i])

            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            gray_image.astype(float)

            for x in range(height):
                for y in range(width):
                    gray_image[x, y] = 1 if (gray_image[x, y] == 0) else 0
            if (i < triangle):
                gray_image = np.append(gray_image.ravel(), 1)
            else:
                gray_image = np.append(gray_image.ravel(), 0)
            target.writerow((gray_image))
"""			
n_of_case = 1000
triangle_size = 0.5
height = 10
width = 10
data_type = 'train'

GenData.GenSet(data_type, n_of_case, triangle_size, height, width)

GenData.Convert2Csv(data_type, n_of_case, triangle_size, height, width)
print("finish")
"""