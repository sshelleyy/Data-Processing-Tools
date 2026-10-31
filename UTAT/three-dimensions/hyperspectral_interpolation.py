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


def upscale_band(my_2Dband):
    "Double 2d band resolution using a two-pass bicubic interpolation."
    """
    Args:
        2d_band (np.ndarray) is 1 'layer' of the cube, shape (h,w)

    Returns:
        np.ndarray: the upscaled band, shape (2h,2w), dtype float32!
    """

    # load band layer
    height, width = my_2Dband.shape

    # make x2 size canvas for new band layer. use float32 for math precision and convert later
    newHeight = height * 2
    newWidth = width * 2
    upscaled = np.zeros((newHeight, newWidth), dtype=np.float32)

    # put "known" pixels (every 2nd pixel)
    upscaled[::2, ::2] = my_2Dband

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

    return upscaled


def upscale_hyperspectral(inputPath, outputPath):
    "Double cube resolution band by band, saving to output .npy file."
    """
    Args:
        inputPath (str): Path to the source .npy file, shape (h,w,b) file.
        outputPath (str): Path to save the 2x upscaled result (2h,2w,b)
    """

    # load cube
    cube = np.load(inputPath)
    if cube is None:
        print("Error: input file doesn't exist")
        return

    height, width, bands = cube.shape

    # make x2 size canvas for new img. use float32 for math precision and convert later
    newHeight = height * 2
    newWidth = width * 2
    upscaled = np.zeros((newHeight, newWidth, bands), dtype=np.float32)

    # loop thru bands and then put in coresponding upscaled
    for b in range(bands):
        singleBand = cube[:, :, b].astype(np.float32)
        upscaled[:, :, b] = upscale_band(singleBand)

    final_cube = np.clip(upscaled, 0, 65535).astype(
        np.uint16
    )  # converted back from float32
    np.save(outputPath, final_cube)
    print("Upscaled cube saved")


def peakVectorRMSE(ref_cube, rec_cube):
    "Computes error between hyperspectral cubes"
    """changed from comparing pixel vals to full spectral vector at each pixel (all bands @ once). also, again, norms by max vector magnitude (so 0<result<1)
    Args:
        ref_cube (numpy.ndarray): The reference cube (h,w,b) file.
        rec_cube (numpy.ndarray): The reconstructed cube (2h,2w,b) file.

    Returns:
        float: The computed RMSE value.

    interpretted from https://github.com/jingmengzhiyue/HyperEvalSR/blob/master/HyperEvalSR/metrics.py
    changed for peak vector RMSE rather than scalar and to compare full spectral vectors rather than pixel values
    """
    if ref_cube.shape != rec_cube.shape:
        raise ValueError(
            "Reference and reconstructed cubes must have the same dimensions."
        )
    if not isinstance(ref_cube, np.ndarray) or not isinstance(rec_cube, np.ndarray):
        raise TypeError("Input images must be numpy arrays.")

    ref_cube = ref_cube.astype(np.float32)
    rec_cube = rec_cube.astype(np.float32)
    diff = ref_cube - rec_cube
    mag = np.linalg.norm(diff, axis=2)
    rmse = np.sqrt(np.mean(mag**2))

    bands = ref_cube.shape[2]
    max = 65535
    peak = np.sqrt(max**2 * bands)
    return rmse / peak


def max_abs_distortion(ref_cube, rec_cube):
    """compute MAD, alternative to PV RMSE

    Args:
        ref_cube (numpy.ndarray): The reference cube (h, w, b).
        rec_cube (numpy.ndarray): The reconstructed cube (h, w, b).

    Returns:
        float: The MAD found between any two corresponding pixels.
    """
    if ref_cube.shape != rec_cube.shape:
        raise ValueError("Cubes must have same dims. ")
    ref_cube = ref_cube.astype(np.float32)
    rec_cube = rec_cube.astype(np.float32)
    abs_diff = np.abs(ref_cube - rec_cube)
    mad = np.max(abs_diff)

    return mad


# run
original_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/indian_pine_array.npy"
og_lowres_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/resized_IPA.npy"
upscaled_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/upscaled_IPA.npy"  # upscaled from compressed file

original = np.load(original_path)

# loading shape. if odd num pixels, crop
h, w, b = original.shape
if h % 2 != 0 or w % 2 != 0:
    original = original[: h - (h % 2), : w - (w % 2), :]
    print(f"Cropped to {original.shape}")

np.save(og_lowres_path, original[::2, ::2, :])
og_lowres = np.load(og_lowres_path)

# peakVectorRMSE compare pixel by pixel so must resize

upscale_hyperspectral(og_lowres_path, upscaled_path)
upscaled = np.load(upscaled_path)

print(
    "MAD Error:",
    (max_abs_distortion(original, upscaled)),
)
print("Peak Vector RMSE:", peakVectorRMSE(original, upscaled))
