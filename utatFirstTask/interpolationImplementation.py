import cv2
import numpy as np


def get_q_coefficients(offset):
    "bicubic interpolation w 4 basis functions: q1,q2,q3,q4"
    offsetPow2 = offset**2
    offsetPow3 = offset**3

    q1 = (-offsetPow3 + 2 * offsetPow2 - offset) / 2
    q2 = (3 * offsetPow3 - 5 * offsetPow2 + 2) / 2
    q3 = (-3 * offsetPow3 + 4 * offsetPow2 + offset) / 2
    q4 = (offsetPow3 - offsetPow2) / 2
    return q1, q2, q3, q4


def upscale_image(inputPath, outputPath):
    # load image
    img = cv2.imread(inputPath)
    if img is None:
        print("Error: input file doesn't exist")
        return

    height, width, channels = img.shape

    # make x2 size canvas for new img. use float32 for math precision and convert later
    newHeight = height * 2
    newWidth = width * 2
    upscaled = np.zeros((newHeight, newWidth, channels), dtype=np.float32)

    # put "known" pixels (every 2nd pixel) from i to o
    for i in range(height):
        for j in range(width):
            upscaled[i * 2, j * 2] = img[i, j]

    # horizonal interpolation
    offset = 0.5
    q1, q2, q3, q4 = get_q_coefficients(offset)

    for i in range(0, newHeight, 2):
        for j in range(1, newWidth, 2):
            if j < 3 or j >= newWidth - 3:  # if edge of pic
                upscaled[i, j] = upscaled[i, j - 1]
            else:  # regular case: use upscale function
                p1 = upscaled[i, j - 3]
                p2 = upscaled[i, j - 1]
                p3 = upscaled[i, j + 1]
                p4 = upscaled[i, j + 3]
                upscaled[i, j] = p1 * q1 + p2 * q2 + p3 * q3 + p4 * q4

    # vertical interpolation
    for j in range(newWidth):
        for i in range(1, newHeight, 2):
            if i < 3 or i >= newHeight - 3:  # if edge of pic
                upscaled[i, j] = upscaled[i - 1, j]
            else:  # regular case: use upscale function
                p1 = upscaled[i - 3, j]
                p2 = upscaled[i - 1, j]
                p3 = upscaled[i + 1, j]
                p4 = upscaled[i + 3, j]
                upscaled[i, j] = p1 * q1 + p2 * q2 + p3 * q3 + p4 * q4

    final_image = np.clip(upscaled, 0, 255).astype(
        np.uint8
    )  # converted back from float32
    cv2.imwrite(outputPath, final_image)
    print("Upscaled image saved")


# run
upscale_image(
    "/Users/shelley/Desktop/pythonFiles/utatFirstTask/skulePhoto.jpg",
    "upscaled_2x_skulePhoto.jpg",
)
