import hyperspectral_interpolation as hi_metrics
import numpy as np
import matplotlib.pyplot as plt


def generate_mad_heatmap(ref_cube, rec_cube):
    """
    visualise MAD in it's spectral band for ref_cube
    Args:
        ref_cube (numpy.ndarray): The reference cube (h, w, b).
        rec_cube (numpy.ndarray): The reconstructed cube (h, w, b).

    Returns:
        Nothing, generates a

    """
    mad_value = hi_metrics.max_abs_distortion(ref_cube, rec_cube)
    diff_cube = np.abs(ref_cube.astype(np.float32) - rec_cube.astype(np.float32))

    # find the band w mad (spatially and spectrally)
    max_idx = np.unravel_index(np.argmax(diff_cube), diff_cube.shape)

    # check if your cube is (H, W, B) or (B, H, W)
    # (H, W, B): the band index is max_idx[2]
    # (B, H, W): the band index is max_idx[0]
    bad_band_idx = max_idx[2]
    error_map = diff_cube[:, :, bad_band_idx]

    # plotting
    plt.figure(figsize=(10, 8))
    plt.imshow(error_map, cmap="inferno")
    plt.colorbar(label="Absolute Intensity Difference")

    plt.title(f"MAD Analysis | Band: {bad_band_idx}\nMax Error Value: {mad_value:.4f}")

    # mark the exact pixel
    """
    plt.annotate(
        "MAD Point",
        xy=(max_idx[1], max_idx[0]),
        xytext=(max_idx[1] + 20, max_idx[0] + 20),
        arrowprops=dict(facecolor="cyan", shrink=0.05),
        color="cyan",
        fontweight="bold",
    )"""

    # Save for documentation
    plt.savefig("mad_heatmap.png", dpi=300)
    plt.show()


# run
original_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/indian_pine_array.npy"
og_lowres_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/resized_IPA.npy"
upscaled_path = "/Users/shelley/Desktop/pythonFiles/utatOnboarding/three-dimensions/sample-data-cubes/indian-pine-files/upscaled_IPA.npy"

original = np.load(original_path)

# loading shape. if odd num pixels, crop
h, w, b = original.shape
if h % 2 != 0 or w % 2 != 0:
    original = original[: h - (h % 2), : w - (w % 2), :]
    print(f"Cropped to {original.shape}")

np.save(og_lowres_path, original[::2, ::2, :])
og_lowres = np.load(og_lowres_path)

# resize

hi_metrics.upscale_hyperspectral(og_lowres_path, upscaled_path)
upscaled = np.load(upscaled_path)

generate_mad_heatmap(original, upscaled)
