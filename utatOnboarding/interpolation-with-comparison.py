import cv2
import numpy as np


def get_q_coefficients(offset):
    "bicubic interpolation w 4 basis functions: q1,q2,q3,q4"
    """ Uses a third-order polynomial to determine the influence (q1-q4)
    of the surrounding four pixels based on the fractional offset.

    Args:
        offset (float): The distance (0 to 1) from the known sample.

    Returns:
        tuple: (q1, q2, q3, q4) coefficients.
    """

    offsetPow2 = offset**2
    offsetPow3 = offset**3

    q1 = (-offsetPow3 + 2 * offsetPow2 - offset) / 2
    q2 = (3 * offsetPow3 - 5 * offsetPow2 + 2) / 2
    q3 = (-3 * offsetPow3 + 4 * offsetPow2 + offset) / 2
    q4 = (offsetPow3 - offsetPow2) / 2
    return q1, q2, q3, q4


def upscale_image(inputPath, outputPath):
    "Double image resolution using a two-pass bicubic interpolation."
    """Maps existing pixels to a 2x grid, then fills horizontal and vertical
    gaps using cubic weighting. Handles boundaries via simple replication.

    Args:
        inputPath (str): Path to the source image file.
        outputPath (str): Path to save the 2x upscaled result.

    Returns:
        None: Saves the image and prints a completion message.
    """

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


def peakVectorRMSE(ref_img, rec_img):
    "Calculate the peak vector rmse between two images"
    """computes RGB vector difference per corresponding pixel, iterating across image, then normalises w max magnitude
    Args:
        ref_img (numpy.ndarray): The reference image.
        rec_img (numpy.ndarray): The reconstructed image.

    Returns:
        float: The computed RMSE value.

    interpretted from https://github.com/jingmengzhiyue/HyperEvalSR/blob/master/HyperEvalSR/metrics.py
    changed for peak vector RMSE rather than scalar
    """
    if ref_img.shape != rec_img.shape:
        raise ValueError(
            "Reference and reconstructed images must have the same dimensions."
        )
    if not isinstance(ref_img, np.ndarray) or not isinstance(rec_img, np.ndarray):
        raise TypeError("Input images must be numpy arrays.")

    ref_img = ref_img.astype(np.float32)
    rec_img = rec_img.astype(np.float32)
    diff = ref_img - rec_img
    mag = np.linalg.norm(diff, axis=2)
    rmse = np.sqrt(np.mean(mag**2))
    peak = np.sqrt(255**2 * 3)
    return rmse / peak


# run
upscale_image(
    "/Users/shelley/Desktop/pythonFiles/utatOnboarding/skulePhoto.jpg",
    "/Users/shelley/Desktop/pythonFiles/utatOnboarding/upscaled_2x_skulePhoto.jpg",
)

original = cv2.imread(
    "/Users/shelley/Desktop/pythonFiles/utatOnboarding/skulePhoto.jpg"
)
reconstructed = cv2.imread(
    "/Users/shelley/Desktop/pythonFiles/utatOnboarding/upscaled_2x_skulePhoto.jpg"
)

original_resized = cv2.resize(  # peakVectorRMSE compare pixel by pixel so must resize
    original,
    (reconstructed.shape[1], reconstructed.shape[0]),
    interpolation=cv2.INTER_CUBIC,
)


print("Peak Vector RMSE:", peakVectorRMSE(original_resized, reconstructed))
