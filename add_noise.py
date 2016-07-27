import numpy as np
import cv2
# import matplotlib.pyplot as plt
from os import listdir, makedirs
from os.path import join, exists
from enum import Enum
import random
import GenData

def openImages(data_type):
    """
    Opening each image in ./image in binary mode
    Return an array of images

    Parameters
    --------------
    images : array of image in ./image folder
    """
    url = "./images/" + data_type
    if not exists(url):
        print('File folder is invalid')
        return -1
    fileList = listdir(url)
    images = []
    kinds = []
    # xu ly RGB ve 255 or 0 truoc khi add vao images
    for i in range(len(fileList)):
        image = cv2.imread(join(url, fileList[i]), 0)
        kinds.append(fileList[i][-6])
        thresh, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        images.append(image)
    return images, kinds

class noiseType(Enum):
    RANDOM = 0      # any where on background point
    ON_EDGE = 1     # on the edge of forceground
    NOT_ON_EDGE = 2 # any where on background (but not on the edge of forceground)


def noiseCount(noiseQuantity, lenBlackPoints, lenWhitePoints):
    """
    Additional function for addNoise function
    To count the number of noise point
    There are 2 types of input (noiseQuantity):
        - int: the exact number of noise point
        - float: the percent of forceground points (black points)
    """
    if type(noiseQuantity) == np.int32:
        return noiseQuantity

    elif type(noiseQuantity) == np.float_:
        return round(noiseQuantity * lenBlackPoints)


def addNoise(images, typeOfNoise):
    """
    Adding noisy data to array of images
    Return new array of images after adding noise

    Parameters
    ------------
    images : array of image from ./image folder
    noiseType : Enum of noiseType class
    noiseQuantity : Float or Int
        Float: percent of black points on image, the percent > 0.0 and <= 1.0 (eg: 0.1, 0.5, 0.8, 0.9 ...)
        Int: the number of noise points (>= 1)

    Another param
    -------------

    """
    if images == -1: return
    noisyImages = []
    for image in images:
        # Preparation
        width = image.shape[1]
        height = image.shape[0]
        blackPoints = [] # Array of forceground point
        whitePoints = [] # Array of background point
        allPoints = []

        for i in range(width):
            for j in range(height):
                allPoints.append(([i, j]))
                if (image[i][j] == 255):
                    whitePoints.append([i, j])
                else:
                    blackPoints.append([i, j])
        noiseQuantity = np.random.random_integers(0, 15)

        noiseNumber = noiseCount(noiseQuantity, len(blackPoints), len(whitePoints))

        if typeOfNoise == noiseType.RANDOM:
            noisePoints = random.sample(allPoints, noiseNumber)
        else:
            # The array of background point that side by forceground
            whiteEdge = []
            # The point not on the edge
            whitePointNotOnEdge = []

            for point in whitePoints:
                x = point[0]
                y = point[1]
                xPlus   = x + 1 - (x + 1) // 9
                xMinus  = abs(x - 1)
                yPlus   = y + 1 - (y + 1) // 9
                yMinus  = abs(y - 1)

                conditions = [
                    image[x][yPlus]         == 0,  image[x][yMinus]        == 0,

                    image[xPlus][y]         == 0,  image[xPlus][yPlus]     == 0,
                    image[xPlus][yMinus]    == 0,

                    image[xMinus][y]        == 0,  image[xMinus][yPlus]    == 0,
                    image[xMinus][yMinus]   == 0
                ]
                if any(conditions): whiteEdge.append([x, y])
                else: whitePointNotOnEdge.append([x, y])

            if typeOfNoise == noiseType.ON_EDGE:
                noisePoints = random.sample(whiteEdge, noiseNumber)
            elif typeOfNoise == noiseType.NOT_ON_EDGE:
                noisePoints = random.sample(whitePointNotOnEdge, noiseNumber)

        for point in noisePoints:
            image[point[0]][point[1]] = np.random.random_integers(0, 255)

        noisyImages.append(image)

    return noisyImages


def writeImages(noisyImages, data_type, kinds):
    url = "./images/" + data_type
    for i in range(len(noisyImages)):
        image = noisyImages[i]
        cv2.imwrite(url + "/%i_%s.jpeg" % (i, kinds[i]), image)

"""
Main Program
"""

n_of_case = 1000
triangle_size = 0.5
height = 10
width = 10
data_type = 'train'

GenData.GenSet(data_type, n_of_case, triangle_size, height, width)

images, kinds = openImages(data_type) # @param : string url original image folder

# @param 0: images the return of function openImage('url')
# @param 1: 1 of 3 type of noise point, => [RAMDOM, ON_EDGE, NOT_ON_EDGE]
# @param 2: 1 of 2 type of noise number => [int: the exact number of noise point; float: [0.0, 1.0] the percent of forceground points]

noisyImages = addNoise(images, noiseType.RANDOM)
writeImages(noisyImages, data_type, kinds)

GenData.Convert2Csv(data_type, n_of_case, triangle_size, height, width)
print("finish")
