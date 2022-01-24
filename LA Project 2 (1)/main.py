from utils import *
import numpy as np
import math
def warpPerspective(img, transform_matrix, output_width, output_height):
    row, col, z = np.shape(img)
    out = np.empty((output_width, output_height, 3), int)
    for i in range(row):
        for j in range(col):
            arr = np.empty((3, 1), int)
            arr[0][0] = i
            arr[1][0] = j
            arr[2][0] = 1
            multipleArr = np.dot(transform_matrix, arr)
            transferesArr = np.empty((2, 1), int)
            transferesArr[0][0] = multipleArr[0][0]/multipleArr[2][0]
            transferesArr[1][0] = multipleArr[1][0]/multipleArr[2][0]
            if (((0 <= transferesArr[0][0]) and (transferesArr[0][0] < 300)) and ((0 <= transferesArr[1][0]) and (transferesArr[1][0] < 400))) :
                out[transferesArr[0][0]][transferesArr[1][0]] = img[i][j]
    return out
    pass


def grayScaledFilter(img):
    transferMatrix = np.array([[0.3, 0.3, 0.3],
                               [0.4, 0.4, 0.4],
                               [0.4, 0.4, 0.4]])
    grayPic = Filter(img, transferMatrix)
    return grayPic
    pass


def crazyFilter(img):
    transferMatrix = np.array([[0, 1, 1],
                               [1, 0, 0],
                               [0, 0, 0]])
    crazyPic = Filter(img, transferMatrix)
    return crazyPic
    pass


def customFilter(img):
    transferMatrix = np.array([[1, 0, 0],
                               [0, 1, 0],
                               [0, 1, 1]])
    filteredImg = Filter(img, transferMatrix)
    showImage(filteredImg, "custom filter", True)

    invereMatrix = np.linalg.inv(transferMatrix)
    unFilteredImg = Filter(filteredImg, invereMatrix)
    showImage(unFilteredImg, "remove custom filter", True)
    pass


def scaleImg(img, scale_width, scale_height):
    row, col, z = np.shape(img)
    scaledImg = np.empty((row * scale_height, col * scale_width, z), int)
    for x in range(row):
        for y in range(col):
            xPrim = math.floor(x * scale_height)
            yPrim = math.floor(y * scale_width)
            scaledImg[xPrim][yPrim] = img[x][y]
            for i in range(scale_height):
                for j in range(scale_width):
                    xAfterPrim = xPrim+i
                    yAfterPrim = yPrim+j
                    scaledImg[xAfterPrim][yAfterPrim] = scaledImg[xPrim][yPrim]
    return scaledImg
    pass


def cropImg(img, start_row, end_row, start_column, end_column):
    croppedImage = img[start_column:end_column, start_row:end_row]
    return croppedImage
    pass


if __name__ == "__main__":
    image_matrix = get_input('pic.jpg')

    # You can change width and height if you want
    width, height = 300, 400

    showImage(image_matrix, title="Input Image")

    # TODO : Find coordinates of four corners of your inner Image ( X,Y format)
    #  Order of coordinates: Upper Left, Upper Right, Down Left, Down Right
    pts1 = np.float32([[106, 213], [378, 179], [159, 644], [497, 570]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    m = getPerspectiveTransform(pts1, pts2)

    warpedImage = warpPerspective(image_matrix, m, width, height)
    showWarpPerspective(warpedImage)

    # grayScalePic = grayScaledFilter(warpedImage)
    # showImage(grayScalePic, title="Gray Scaled")

    crazyImage = crazyFilter(warpedImage)
    showImage(crazyImage, title="Crazy Filter")

    customFilter(warpedImage)

    croppedImage = cropImg(warpedImage, 50, 300, 50, 225)
    showImage(croppedImage, title="Cropped Image")

    scaledImage = scaleImg(warpedImage, 2, 3)
    showImage(scaledImage, title="Scaled Image")
